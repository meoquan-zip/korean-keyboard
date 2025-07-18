# Korean Keyboard

A Python package that replicates the behaviour of the standard Korean (Hangul) keyboard layout. Designed to convert
Latin keystrokes (e.g. `r`, `g`, `k`, `s`) into properly composed Korean syllables (e.g. `가`, `한`) using Unicode
algorithmic composition.

---

## Understanding Hangul and the Dubeolsik Layout

**Hangul (한글)** is the Korean alphabet system. It was created in the 15th century and is known for its scientific
design and ease of learning. Each syllable is formed by combining at least one consonant and one vowel, grouped into a
square block like `가`, `한`, or `문`.

If you are new to Hangul, we recommend reading this guide:
[Korean Alphabet – Learn the Hangul Letters and Character Sounds](https://www.90daykorean.com/how-to-learn-the-korean-alphabet/)

### The Dubeolsik Keyboard Layout

The most common Korean keyboard layout is the **Dubeolsik (두벌식)** or **two-set layout**. It was officially
standardised in 1969 by the South Korean government, mainly for its simplicity and compatibility with typewriters and
early computers.

![Dubeolsik layout](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/blogs/2147503409/images/g1AG22jzRAa0ZXXJZaa3_3.png)

<sub>_Image source: [goodjobkorean.com](https://www.goodjobkorean.com/blog/how-to-type-in-korean-with-your-phone-tablet-and-computer)_</sub>

Here is how the Dubeolsik layout works:
- **Consonants** are arranged on the left side;
- **Vowels** are arranged on the right side;
- **Double consonants** (`ㄲ`, `ㄸ`, `ㅃ`, `ㅆ`, `ㅉ`) and **additional vowels** (`ㅒ`, `ㅖ`) can be typed by holding
`Shift` while pressing certain keys.

---

## Installation

### 1. Clone the repository

Open your terminal or Git Bash, navigate to your desired project directory, then run:

```bash
git clone https://github.com/meoquan-zip/korean-keyboard.git
```

This creates a `korean-keyboard/` folder in your current directory.

### 2. Install the package in editable mode

Navigate into the folder (or any subdirectory within it) and run:

```bash
pip install -e .
```

This allows you to make changes to the code and immediately reflect them without reinstalling.

---

## Usage

Once installed, you can use the package in any Python script or notebook:

```python
from koreankb import Keyboard

kb = Keyboard()

# combines letters to form hangul syllables
kb.input('dl')     # 'ㅇ' + 'ㅣ' → '이'
kb.input('w')      # '이' + 'ㅈ' → '잊'
print(kb)          # '잊'

# final of last syllable becomes initial of new syllable when medial follows
kb.input('l')      # '잊' + 'ㅣ' → '이지'
print(kb)          # '이지'

# deletes last `length` inputs (`length` is 1 by default)
kb.backspace(2)    # '이지' → '이'
print(kb)          # '이'
kb.backspace()     # '이' → ''
print(kb)          # ''
```

For more examples, see the included [`test.ipynb`](./test.ipynb).

---

## Requirements

- Python 3.7+

No additional dependencies.

---

## Future Plans

This package currently supports only keystroke-to-Hangul conversion. In the future, it may expand to include:

- Romanisation (Hangul → Latin)
- Translation modules (Korean ↔ English)
- Input normalisation and prediction
