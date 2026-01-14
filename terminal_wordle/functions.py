import os
import sys
import random
import requests
import socket
import csv
from colorama import init, Fore, Back, Style
import re

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
    filedescriptors = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

        
init(autoreset=True)

colour_priority = {
    "<bg-green>": 3,
    "<bg-yellow>": 2,
    "<bg-black>": 1
}

def get_single_keypress():
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8')
    else: 
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
def colour_print(text, foot=None):
    tag_to_style = {
        "<red>": Fore.RED,
        "<cyan>": Fore.CYAN,
        "<green>": Fore.GREEN,
        "<yellow>": Fore.YELLOW,
        "<bg-green>": Back.GREEN,
        "<bg-yellow>": Back.YELLOW,
        "<bg-black>": Back.BLACK,
        "<bg-white>": Back.WHITE,
        "<magenta>": Fore.MAGENTA,
        "<black>": Fore.BLACK,
        "<bold>": Style.BRIGHT,
        "<reset>": Style.RESET_ALL
    }

    for tag, style in tag_to_style.items():
        text = text.replace(tag, style)

    if foot is None:
        print(text)
    else:
        print(text, end = foot)
    
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_words_by_difficulty(file_path):
    words_by_difficulty = {i: [] for i in range(1, 10)}
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        words = [row for row in csv_reader if int(row[1]) > 0]
        target_size = len(words) // 8

        csv_file.seek(0)
        next(csv_reader)

        cursor = 1
        for row in csv_reader:
            word, frequency = row[0].lower(), int(row[1])
            if frequency == 0:
                words_by_difficulty[9].append(word)
            else:
                words_by_difficulty[cursor].append(word)
                if len(words_by_difficulty[cursor]) >= target_size and cursor < 8:
                    cursor += 1

    return words_by_difficulty

def check_word(word):
    with open('words.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for li in csv_reader:
            if word in li[0].lower():
                return True
    return False

def isConnect():
    try:
        s = socket.create_connection(("www.google.com", 80))
        if s is not None:
            s.close()
        return True
    except OSError:
        pass
    return False

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list):
            word_info = data[0]
            phonetic = word_info.get("phonetic", "")
            meanings = word_info.get("meanings", [])
            if meanings:
                first_meaning = meanings[0]
                part_of_speech = first_meaning.get("partOfSpeech", "")
                definitions = first_meaning.get("definitions", [])
                if definitions:
                    first_definition = definitions[0].get("definition", "No definition available.")
                    example = definitions[0].get("example", "No example available.")

                    return {
                        "word": word,
                        "phonetic": phonetic,
                        "part_of_speech": part_of_speech,
                        "definition": first_definition,
                        "example": example
                    }
        return None
    except requests.RequestException as e:
        print(f"Error fetching definition: {e}")
        return None
    
def print_board(main, keys):
    for i in range(6):
        row = i + 1
        col1 = f"{row}: "
        col2 = ""
        for letter in main[str(i+1)]:
            col2 = col2 + " " + letter + " "
        col3 = ""
        if i % 2 == 0:
            line = keys[i//2]
            for j in line:
                if j.isdigit():
                    col3 = col3 + "   "
                elif "*" in line[j]:
                    col3 = col3 + " " + "<black><bg-white>" + j + "<reset>" + " "
                else:
                    col3 = col3 + " " + line[j] + j + "<reset>" + " "
        colour_print("%-5s %-10s %-8s %s" %(col1, col2, "", col3))

def exit_program():
    if os.name == "nt": 
        os.system("taskkill /F /IM cmd.exe")
    elif os.name == "posix":
        if sys.platform == "darwin":
            os.system("osascript -e 'tell application \"Terminal\" to close (every window whose name contains \"Python\")'")
        else: 
            os.system("kill -9 $PPID")

    sys.exit()
