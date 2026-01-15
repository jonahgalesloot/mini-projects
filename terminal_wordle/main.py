import functions

functions.cls()
wordlist = functions.load_words_by_difficulty("words.csv")

while True:
    title = "Welcome to Wordle"
    while True:
        functions.cls()
        functions.colour_print(
            f"<green>{title}<reset>\n"
            "[<cyan>1<reset>] Play Game\n"
            "[<magenta>2<reset>] Tutorial\n"
            "[<yellow>3<reset>] Quit\n"
            ,"\n")
        try:
            diff = functions.get_single_keypress()
            if diff in ("1","2","3"):
                break
            else:
                title = "Please pick a valid choice"
        except UnicodeDecodeError:
            continue

    if diff == '2':
        functions.cls()
        functions.colour_print(
            "<magenta>Wordle Tutorial<reset>\n"
            "Wordle is a word-guessing game where you have six tries to guess a 5-letter word.\n"
            "Each letter of your guess will be color-coded to help you:\n"
            " - <bg-green>Green<reset>: Correct letter in the correct position.\n"
            " - <bg-yellow>Yellow<reset>: Correct letter, wrong position.\n"
            " - <bg-black>Gray<reset>: Letter not in the word.\n"
            "Press any key to return to the main menu."
        )
        try:
            functions.get_single_keypress()
        except UnicodeDecodeError:
            pass
        continue

        

    if diff == '3':
        break

    board = ["Easy"] + ["-" for _ in range(9)] + ["Hard"]
    cursor = 2
    while True:
        functions.cls()
        functions.colour_print(
            "<cyan>Choose your difficulty<reset>\n"
            "[<cyan>A<reset>] for easier, [<cyan>D<reset>] for harder, [<cyan>Enter<reset>] to submit\n"
            ,"")
        board_display = ""
        for i in range(len(board)):
            if i == cursor - 1:
                if cursor-1 > 6:
                    colour_diff = "red"
                elif cursor-1 > 3:
                    colour_diff = "yellow"
                else:
                    colour_diff = "green"
                board_display += f"[<{colour_diff}>#<reset>] "
            else:
                board_display += board[i] + " "
        functions.colour_print(board_display,"")
        try:
            move = functions.get_single_keypress()
            if move.lower() == "a" and cursor > 2:
                cursor -= 1
            elif move.lower() == "d" and cursor < len(board) - 1:
                cursor += 1
            elif move == "\r":
                break
        except UnicodeDecodeError:
            continue

    answer = #wordlist[cursor - 1][functions.random.randint(0, len(wordlist[cursor - 1]) - 1)]
    guesses = {
        '1': ['.', '.', '.', '.', '.'],
        '2': ['.', '.', '.', '.', '.'],
        '3': ['.', '.', '.', '.', '.'],
        '4': ['.', '.', '.', '.', '.'],
        '5': ['.', '.', '.', '.', '.'],
        '6': ['.', '.', '.', '.', '.']
    }
    keyboard = [
        {"q":"<reset>","w":"<reset>","e":"<reset>","r":"<reset>","t":"<reset>","y":"<reset>","u":"<reset>","i":"<reset>","o":"<reset>","p":"<reset>"},
        {"1":"<reset>","a":"<reset>","s":"<reset>","d":"<reset>","f":"<reset>","g":"<reset>","h":"<reset>","j":"<reset>","k":"<reset>","l":"<reset>"},
        {"2":"<reset>","z":"<reset>","x":"<reset>","c":"<reset>","v":"<reset>","b":"<reset>","n":"<reset>","m":"<reset>","2":"<reset>"}
    ]

    functions.cls()
    functions.colour_print(f"<{colour_diff}>Guess a 5 letter word:<reset>")
    functions.print_board(guesses, keyboard)

    currentY = 1
    currentX = 0

    while True:
        try:
            keypress = functions.get_single_keypress()
            if keypress.isalpha() and not ('\xe0' in keypress or '\x00' in keypress):
                keypress = keypress.lower()
                for l in keyboard:
                    try:
                        l[guesses[str(currentY)][currentX]] = l[guesses[str(currentY)][currentX]].replace("<*","<")
                    except:
                        continue
                guesses[str(currentY)][currentX] = keypress
                for l in keyboard:
                    try:
                        l[keypress] = l[keypress].replace("<","<*")
                    except:
                        continue
                if currentX < 4:
                    currentX += 1
                functions.cls()
                functions.colour_print(f"<{colour_diff}>Guess a 5 letter word:<reset>")
                functions.print_board(guesses, keyboard)
            elif keypress == "\b":
                if currentX == 4 and guesses[str(currentY)][4] != '.':
                    currentX = 4
                elif currentX > 0:
                    currentX -= 1
                for l in keyboard:
                    try:
                        l[guesses[str(currentY)][currentX]] = l[guesses[str(currentY)][currentX]].replace("<*","<")
                    except:
                        continue
                guesses[str(currentY)][currentX] = '.'
                
                functions.cls()
                functions.colour_print(f"<{colour_diff}>Guess a 5 letter word:<reset>")
                functions.print_board(guesses, keyboard)
            elif keypress == '\r':
                word_guess = ''.join(guesses[str(currentY)])
                word_cleaned = functions.re.sub(r"<[^>]*>", "", word_guess)
                for l in keyboard:
                    for t in l:
                        l[t].replace("<*","<")
                if functions.check_word(word_cleaned):
                    answer_count = {}
                    for letter in answer:
                        answer_count[letter] = answer_count.get(letter, 0) + 1
                    keyboard_colors = {}
                    for letter in range(5):
                        guess_letter = guesses[str(currentY)][letter]
                        if guess_letter == answer[letter]:
                            guesses[str(currentY)][letter] = f"<bg-green>{guess_letter}<reset>"
                            answer_count[guess_letter] -= 1
                            keyboard_colors[guess_letter] = "<bg-green>"
                    for letter in range(5):
                        guess_letter = guesses[str(currentY)][letter]
                        if guess_letter != answer[letter] and guess_letter in answer_count and answer_count[guess_letter] > 0:
                            guesses[str(currentY)][letter] = f"<bg-yellow>{guess_letter}<reset>"
                            answer_count[guess_letter] -= 1
                            if guess_letter not in keyboard_colors:
                                keyboard_colors[guess_letter] = "<bg-yellow>"
                    for letter in range(5):
                        guess_letter = guesses[str(currentY)][letter]
                        if guess_letter != answer[letter] and (guess_letter not in answer or answer_count[guess_letter] == 0):
                            guesses[str(currentY)][letter] = f"<bg-black>{guess_letter}<reset>"
                            if guess_letter not in keyboard_colors:
                                keyboard_colors[guess_letter] = "<bg-black>"
                    for row in keyboard:
                        for key in row:
                            if key in keyboard_colors:
                                current_color = row[key]
                                if functions.colour_priority[keyboard_colors[key]] > functions.colour_priority.get(current_color, 0):
                                    row[key] = keyboard_colors[key]
                    
                    functions.cls()
                    functions.colour_print(f"<{colour_diff}>Guess a 5 letter word:<reset>")
                    functions.print_board(guesses, keyboard)
                    currentX = 0
                    currentY += 1
                    if word_cleaned == answer:
                        functions.cls()
                        functions.colour_print(f"You Win!")
                        functions.print_board(guesses, keyboard)
                        break
                    if currentY > 6:
                        functions.cls()
                        functions.colour_print(f"<cyan>You Lose! The word was <reset>{answer}")
                        functions.print_board(guesses, keyboard)
                        break
                else:
                    functions.cls()
                    guesses[str(currentY)] = ['.', '.', '.', '.', '.']
                    currentX = 0
                    functions.colour_print(f"Not in word list")
                    functions.print_board(guesses, keyboard)
        except UnicodeDecodeError:
            continue

    if functions.isConnect():
        print(f"\n{functions.Fore.CYAN}Would you like to see the definition of the word? (y/n){functions.Style.RESET_ALL}")
        try:
            see_definition = functions.get_single_keypress()
            if see_definition.lower() == 'y':
                definition_info = functions.get_word_definition(answer)
                if definition_info:
                    print(f"\nDefinition of '{answer}':")
                    part_of_speech = definition_info.get("part_of_speech", "Unknown").capitalize()
                    def_text = definition_info.get("definition", "No definition available.")
                    example = definition_info.get("example", "No example available.")
                    print(f"\n{functions.Fore.WHITE}{part_of_speech}: {def_text}{functions.Style.RESET_ALL}")
                    print(f"Example: {functions.Fore.WHITE}{example}{functions.Style.RESET_ALL}")
                else:
                    print(f"{functions.Fore.WHITE}No definition found for '{answer}'.{functions.Style.RESET_ALL}")
                print("\nPress any key to return to the main menu.")
                functions.get_single_keypress()
            else:
                print("\nReturning to the main menu...")
        except UnicodeDecodeError:
            continue
    else:
        print(f"\n{functions.Fore.CYAN}Please connect to internet to see dictionary word{functions.Style.RESET_ALL}\nPress any key to return to the main menu.")
        functions.get_single_keypress()

print("Thanks for Playing ;)")

functions.exit_program()
