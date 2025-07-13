from load_data import *


class KoreanKeyboard:
    def __init__(self, string='', cursor=''):
        self.__keymap = load_keymap()
        self.__consonants = load_consonants()
        self.__vowels = load_vowels()
        self.__mergemap = load_mergemap()
        self.__splitmap = {v: k for k, v in self.__mergemap.items()}
        self.__hasfinal = False
        self.string = string
        self.cursor = cursor

    def __str__(self):
        return self.string + self.cursor

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
                self.string += self.cursor + char
                self.cursor = ''
                self.__hasfinal = False
                continue

            if self.cursor == '':
                self.cursor = c
                self.__hasfinal = False
                continue

            if self.__hasfinal and c in self.__vowels:
                h1, h2 = self.__split(self.cursor)
                self.string += h1
                self.cursor = h2

            han = self.__merge(self.cursor, c)

            if han is not None:
                self.cursor = han
            else:
                self.string += self.cursor
                self.cursor = c

            self.__hasfinal = c in self.__consonants and c != self.cursor

    def backspace(self, length=1):
        for _ in range(length):
            if self.cursor == '':
                self.string = self.string[:-1]
                self.__hasfinal = False
            else:
                split = self.__split(self.cursor)
                if split is None:
                    self.cursor = ''
                    self.__hasfinal = False
                else:
                    self.cursor = split[0]
                    split = self.__split(self.cursor)
                    self.__hasfinal = split is not None and split[1] in self.__consonants
