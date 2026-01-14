# Terminal Wordle

## Purpose  
One of my older projects, a full terminal implementation of Wordle with custom color-coded ANSI output, difficulty selection, persistent keyboard state, and dictionary lookup integration. This one stands out from many of my other projects due to the amount of time put into polish beyond core functionality: terminal UI navigation, visual feedback, and user experience details. This is still my most polished project, where extra effort went into aesthetics (color persistence, smooth navigation, tutorial) rather than algorithmic complexity, making a responsive UI that transcends most of my Python CLI projects. 


## Data Sources
- Word frequency list (words.csv)
12,901 five-letter English words ranked by literature frequency .
- Source: wordsrated.com (originally scraped via Selenium automation, though I no longer have access to the original script). Site rebranded to wordraiders.com/wordlists/5-letter-words/. Used the Google Books Ngram English Corpus for rating frequency of words occurence.

## How It Works  
- Cross-platform keypress capture (`msvcrt` Windows / `termios` Unix) for real-time input.  
- Colorama-powered ANSI coloring simulates Wordle feedback (green/yellow/gray).  
- 9 difficulty levels from `words.csv` frequency data (easy = common words, hardest is words with 0 recorded uses).  
- Keyboard maintains persistent color state across guesses (green > yellow > gray priority).  
- Post-game dictionary API lookup with part-of-speech + example sentences.

## Included Files  
- `main.py`: Core game loop, difficulty selector, guess validation, win/lose logic.  
- `functions.py`: Terminal utilities (keypress, ANSI colors, word loading, dictionary API).  
- `words.csv`: Word frequency data for difficulty bucketing.

## Prerequisites  
- Python 3.10+  
- `pip install colorama requests screeninfo opencv-python pygame numpy`

## Usage  
```bash
python main.py
```

## Features
1. Main menu → Tutorial/Quit
2. Arrow-key difficulty selector (A/D + Enter) w/ color-coded cursor
3. Real-time typing + backspace on 6x5 grid
4. Keyboard color updates (persists across rows)
5. Dictionary lookup after win (y/n prompt)
6. 'q' to quit any screen
