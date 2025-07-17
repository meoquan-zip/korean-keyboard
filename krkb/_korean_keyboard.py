from ._load_data import load_keymap, load_initials, load_medials, load_finals, load_bindmap


class Keyboard:
    def __init__(self):
        self.__KEYMAP = load_keymap()
        self.__INITIALS = load_initials()
        self.__MEDIALS = load_medials()
        self.__FINALS = load_finals()
        self.__BINDMAP = load_bindmap()
        self.__SPLITMAP = {v: k for k, v in self.__BINDMAP.items()}

        self._string = ''
        self._initial = None
        self._medial = None
        self._final = None

    def __str__(self):
        return self._string + self.__compose()

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'_string={self._string!r}, '
                f'_buffer={self.__compose()!r})')

    def __isempty(self) -> bool:
        return not (self._initial or self._medial or self._final)

    def __iscomplete(self) -> bool:
        return self._initial and self._medial

    def __compose(self) -> str:
        if not self.__iscomplete():
            return ''.join(filter(None, [
                self._initial, self._medial, self._final
            ]))

        ini = self.__INITIALS[self._initial]
        med = self.__MEDIALS[self._medial]
        fin = self.__FINALS[self._final]

        return chr(0xAC00 + ini * 21 * 28 + med * 28 + fin)

    def __flush(self):
        hangul = self.__compose()

        if hangul:
            self._string += hangul

        self._initial = None
        self._medial = None
        self._final = None

    def input(self, text: str):
        for char in text:
            entry = self.__KEYMAP.get(char)

            # not hangul letter typed from keyboard
            if entry is None:
                self.__flush()
                self._string += char
                continue

            letter, category = entry

            # buffer is empty
            if self.__isempty():
                if 'ini' in category:
                    self._initial = letter
                else:
                    self._medial = letter
                continue

            # buffer has final
            if self._final:
                if 'med' in category:
                    split = self.__SPLITMAP.get(self._final)
                    if split is None:
                        tmp = self._final
                        self._final = None
                    else:
                        self._final, tmp = split
                    self.__flush()
                    self._initial = tmp
                    self._medial = letter
                else:
                    comb = (self._final, letter)
                    if comb in self.__BINDMAP:
                        self._final = self.__BINDMAP[comb]
                    else:
                        self.__flush()
                        self._initial = letter
                continue

            # buffer has medial, no final
            if self._medial:
                if 'fin' in category:
                    self._final = letter
                elif 'med' in category:
                    comb = (self._medial, letter)
                    if comb in self.__BINDMAP:
                        self._medial = self.__BINDMAP[comb]
                    else:
                        self.__flush()
                        self._medial = letter
                else:
                    self.__flush()
                    self._initial = letter
                continue

            # buffer has initial, no medial or final
            if 'med' in category:
                self._medial = letter
            else:
                comb = (self._initial, letter)
                if comb in self.__BINDMAP:
                    self._initial = None
                    self._final = self.__BINDMAP[comb]
                else:
                    self.__flush()
                    self._initial = letter

    def backspace(self, length=1):
        for _ in range(length):
            # buffer has final
            if self._final:
                split = self.__SPLITMAP.get(self._final)
                if split:
                    self._final = split[0]
                else:
                    self._final = None
                continue

            # buffer has medial, no final
            if self._medial:
                split = self.__SPLITMAP.get(self._medial)
                if split:
                    self._medial = split[0]
                else:
                    self._medial = None
                continue

            # buffer has initial, no medial or final
            if self._initial:
                self._initial = None
                continue

            # buffer is empty
            self._string = self._string[:-1]

