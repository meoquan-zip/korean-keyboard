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

    def __is_empty(self) -> bool:
        """Checks whether the Hangul input buffer is empty.

        Returns:
            bool: True if none of `_initial`, `_medial`, or `_final` is set; False otherwise.
        """
        return not (self._initial or self._medial or self._final)

    def __is_complete(self) -> bool:
        """Checks whether the Hangul input buffer is complete.

        A complete Hangul syllable must have at least one consonant (initial) and one vowel (medial).

        Returns:
            bool: True if both `_initial` and `_medial` are set, False otherwise.
        """
        return self._initial and self._medial

    def __compose(self) -> str:
        """Composes and returns the Hangul syllable from the current Hangul input buffer.

        If the buffer does not contain a complete syllable (e.g. missing an initial or medial), the method returns the
        non-empty components joined together in order. If the buffer forms a complete Hangul syllable, it calculates
        and returns the corresponding Unicode character. If the buffer is empty, an empty string is returned.

        Returns:
            str: A Hangul syllable, partial sequence of Hangul letters (jamo), or an empty string.
        """
        if not self.__is_complete():
            return ''.join(filter(None, [
                self._initial, self._medial, self._final
            ]))

        ini = self.__INITIALS[self._initial]
        med = self.__MEDIALS[self._medial]
        fin = self.__FINALS[self._final]

        return chr(0xAC00 + ini * 21 * 28 + med * 28 + fin)

    def __flush(self) -> None:
        """Finalises and resets the current Hangul input buffer.

        The composed Hangul string, if not empty, is appended to the main output string. The buffer is then reset by
        clearing the initial, medial, and final components.

        Returns:
            None
        """
        hangul = self.__compose()

        if hangul:
            self._string += hangul

        self._initial = None
        self._medial = None
        self._final = None

    def input(self, text: str) -> None:
        """Processes input text and updates the internal Hangul string.

        This method simulates typing on a Korean keyboard. Each character in the input string is examined individually.
        If it is a basic English letter (A–Z or a–z), it is mapped to a corresponding Hangul keystroke using the
        standard Dubeolsik layout and composed into valid syllables. Any other character (such as numbers, punctuation,
        whitespace, or extended Latin characters) is inserted as-is without modification.

        Args:
            text (str): Input text string.

        Returns:
            None: Use `str(self)` to view the updated Hangul string.
        """
        for char in text:
            entry = self.__KEYMAP.get(char)

            # not hangul letter typed from keyboard
            if entry is None:
                self.__flush()
                self._string += char
                continue

            letter, category = entry

            # buffer is empty
            if self.__is_empty():
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

    def backspace(self, length=1) -> None:
        """Deletes input and updates the internal Hangul string.

        This method simulates deleting most recent `length` keystrokes as if pressing the backspace key `length` times.
        Hangul syllables that are still in the internal buffer are broken down one letter at a time. Once the buffer is
        empty, additional deletions will directly remove whole characters from the finalised output string.

        Args:
            length (int): The number of keystroke units to delete (default is 1).

        Returns:
            None: Use `str(self)` to view the updated Hangul string.
        """
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
