import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hangul.db')


def load_keymap() -> dict[str, str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT key, hangul
        FROM letters
    """)
    keymap = {key: hangul for key, hangul in cur.fetchall()}
    con.close()
    return keymap


def load_consonants() -> set[str]:
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


def load_vowels() -> set[str]:
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


def load_mergemap() -> dict[tuple[str, str], str]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT *
        FROM merge_table
    """)
    mergemap = {(h1, h2): hangul for h1, h2, hangul in cur.fetchall()}
    con.close()
    return mergemap
