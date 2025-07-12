import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hangul.db')


def get_keymap() -> dict[str, str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT key, hangul
        FROM letters
    """)
    keymap = {key: hangul for key, hangul in cur.fetchall()}
    con.close()
    return keymap


def get_consonants() -> set[str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT DISTINCT hangul
        FROM letters
        WHERE type = 'consonant'
    """)
    consonants = {row[0] for row in cur.fetchall()}
    con.close()
    return consonants


def get_vowels() -> set[str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT DISTINCT hangul
        FROM letters
        WHERE type = 'vowel'
    """)
    vowels = {row[0] for row in cur.fetchall()}
    con.close()
    return vowels


def get_mergemap() -> dict[tuple[str, str], str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT *
        FROM merge_table
    """)
    mergemap = {(h1, h2): hangul for h1, h2, hangul in cur.fetchall()}
    con.close()
    return mergemap


class KoreanKeyboard:
    def __init__(self):
        self.__keymap = get_keymap()
        self.__consonants = get_consonants()
        self.__vowels = get_vowels()
        self.__mergemap = get_mergemap()
        self.__splitmap = {v: k for k, v in self.__mergemap.items()}
        self.__string = ''
        self.__cursor = ''
        self.__hasfinal = False

    def __str__(self):
        return self.__string + self.__cursor

    def __merge(self, h1: str, h2: str) -> str | None:
        return self.__mergemap.get((h1, h2))

    def __split(self, hangul: str) -> tuple[str, str] | None:
        return self.__splitmap.get(hangul)

    def _get_properties(self):
        return (
            self.__keymap.copy(),
            self.__consonants.copy(),
            self.__vowels.copy(),
            self.__mergemap.copy(),
            self.__splitmap.copy()
        )

    def input(self, text: str):
        for char in text:
            c = self.__keymap.get(char)

            if c is None:
                self.__string += self.__cursor + char
                self.__cursor = ''
                self.__hasfinal = False
                continue

            if self.__cursor == '':
                self.__cursor = c
                self.__hasfinal = False
                continue

            if self.__hasfinal and c in self.__vowels:
                h1, h2 = self.__split(self.__cursor)
                self.__string += h1
                self.__cursor = h2

            han = self.__merge(self.__cursor, c)

            if han is not None:
                self.__cursor = han
            else:
                self.__string += self.__cursor
                self.__cursor = c

            self.__hasfinal = c in self.__consonants and c != self.__cursor

    def backspace(self, length=1):
        for _ in range(length):
            if self.__cursor == '':
                self.__string = self.__string[:-1]
                self.__hasfinal = False
            else:
                splitted = self.__split(self.__cursor)
                if splitted is None:
                    self.__cursor = ''
                    self.__hasfinal = False
                else:
                    self.__cursor = splitted[0]
                    splitted = self.__split(self.__cursor)
                    self.__hasfinal = splitted is not None and splitted[1] in self.__consonants
