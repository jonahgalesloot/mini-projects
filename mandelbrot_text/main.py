import os
import msvcrt
import colorsys
import pyautogui

def zoomOut():
    old_columns, old_rows = 0, 0
    columns, rows = os.get_terminal_size()
    while old_columns != columns and old_rows != rows:
        pyautogui.hotkey('ctrl', '-')
        old_columns, old_rows = columns, rows
        columns, rows = os.get_terminal_size()

def zoomIn(repetitions):
    columns, rows = os.get_terminal_size()
    while columns > repetitions:
        pyautogui.hotkey('ctrl', '=', "shift")
        columns, rows = os.get_terminal_size()

def render_board(columns, rows, pixel_width, pixel_height, startX, startY):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before starting
    for row_index in range(rows-1):
        line = []
        for column_index in range(columns):
            c = complex(column_index * pixel_width + startX, row_index * pixel_height + startY)
            iteration = check_mandelbrot(c)
            bg_color = get_color(iteration)
            line.append(f"{bg_color} \033[0m")
        
        print(''.join(line), flush=True)



def check_mandelbrot(inpNum):
    num = 0
    for i in range(100):
        num = (num**(2)) + inpNum
        if abs(num) > 2:
            return i
    return -1

def get_color(iteration, max_iteration=100):
    """
    prim = random.randint(1, 6)
    if prim == 1:  # Red
        r, g, b = 1, 0, 0
    elif prim == 2:  # Green
        r, g, b = 0, 1, 0
    elif prim == 3:  # Blue
        r, g, b = 0, 0, 1
    elif prim == 4:  # Cyan
        r, g, b = 0, 1, 1
    elif prim == 5:  # Magenta
        r, g, b = 1, 0, 1
    elif prim == 6:  # Yellow
        r, g, b = 1, 1, 0
    if iteration == -1:
        return f"\033[48;2;{r * 255};{g * 255};{b * 255}m"
    
    """
    if iteration == -1:
        return "\033[40m"
    hue = (iteration / max_iteration) * 0.8
    r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
    return f"\033[48;2;{r};{g};{b}m"


def make_board(columns, rows, pixel_width, pixel_height, startX, startY, cursorX, cursorY):
    board = [[" " for i in range(columns)] for j in range(rows)]
    for row_index in range(rows):
        for column_index in range(columns):
            c = complex(column_index * pixel_width + startX, row_index * pixel_height + startY)
            iteration = check_mandelbrot(c)
            bg_color = get_color(iteration)
            if int(row_index) == int(cursorY) and int(column_index) == int(cursorX) - 1:
                char = "╔"
            elif int(row_index) == int(cursorY) + 1 and int(column_index) == int(cursorX) - 1:
                char = "╚"
            elif int(row_index) == int(cursorY) and int(column_index) == int(cursorX):
                char = "═"
            elif int(row_index) == int(cursorY) + 1 and int(column_index) == int(cursorX):
                char = "═"
            elif int(row_index) == int(cursorY) + 1 and int(column_index) == int(cursorX) + 1:
                char = "╝"
            elif int(row_index) == int(cursorY) and int(column_index) == int(cursorX) + 1:
                char = "╗"
            else:
                char = " "
            if bg_color.startswith("\033[48;2;") and bg_color.endswith("m"):
                rgb = bg_color[7:-1].split(';')
                try:
                    r, g, b = map(int, rgb)
                except ValueError:
                    r, g, b = 0, 0, 0
            else:
                r, g, b = 0, 0, 0
            r, g, b = 255 - r, 255 - g, 255 - b
            fg_color = f"\033[38;2;{r};{g};{b}m"
            board[row_index][column_index] = f"{bg_color}{fg_color}{char}\033[0m"
    controls = [
        "┌────────────────────┐",
        "│      Controls      │",
        "│ W: Up    S: Down   │",
        "│ A: Left  D: Right  │",
        "│ 9: Zoom in         │",
        "│ 0: Zoom out        │",
        "│ Shift: Fine control│",
        "│ R: Render Fractal  │",
        "│ 1/2: Increase /    │",
        "│      Resolution    │",
        "│ E: Exit            │",
        "└────────────────────┘"
    ]
    for i, line in enumerate(controls):
        for j, char in enumerate(line):
            if i < rows and j < len(line):
                board[i][columns - len(line) + j] = f"\033[7m{char}\033[0m"
    return board

def print_board(board):
    os.system("cls" if os.name == "nt" else "clear")
    for i in range(len(board) - 1):
        for j in board[i]:
            print(j, end="")
        print()
    for j in board[-1]:
        print(j, end="")
    print(end="", flush=True)

fast_move_speed = 3
slow_move_speed = 1
fast_zoom_speed = 2
slow_zoom_speed = 2**.5

os.system('cls')

columns, rows = os.get_terminal_size()

zoom_factor = 1.0
startX, startY = -2, -1
pixel_width = 3 / (columns * zoom_factor)
pixel_height = 2 / (rows * zoom_factor)
cursorX = columns / 2
cursorY = rows / 2
print_board(make_board(columns, rows, pixel_width, pixel_height, startX, startY, cursorX, cursorY))

while True:
    old_columns, old_rows = columns, rows
    if msvcrt.kbhit():
        try:
            move = msvcrt.getch().decode()
            if move == "1":
                pyautogui.hotkey('ctrl', '=', "shift")
                columns, rows = os.get_terminal_size()
            if move == "2":
                pyautogui.hotkey('ctrl', '-')
                columns, rows = os.get_terminal_size()
            if move.lower() == "e":
                break
            if move.lower() == 'r':
                os.system("cls")
                print("Loading...")
                old_col, old_row = os.get_terminal_size()
                zoomOut()
                columns, rows = os.get_terminal_size()
                pixel_width = 3 / (columns * zoom_factor)
                pixel_height = 2 / (rows * zoom_factor)
                render_board(columns, rows, pixel_width, pixel_height, startX, startY)
                msvcrt.getch()
                os.system("cls")
                print("Loading...")
                zoomIn(old_col)
                columns, rows = os.get_terminal_size()
                cursorX = (cursorX / old_columns) * columns
                cursorY = (cursorY / old_rows) * rows
                pixel_width = 3 / (columns * zoom_factor)
                pixel_height = 2 / (rows * zoom_factor)
                print_board(make_board(columns, rows, pixel_width, pixel_height, startX, startY, cursorX, cursorY))
            if move.lower() in ['w', 's', 'a', 'd']:
                move_speed = slow_move_speed if move.isupper() else fast_move_speed
                if move.lower() == 'w':
                    startY -= pixel_height * move_speed
                elif move.lower() == 's':
                    startY += pixel_height * move_speed
                elif move.lower() == 'a':
                    startX -= pixel_width * move_speed
                elif move.lower() == 'd':
                    startX += pixel_width * move_speed
            elif move in ['9', '(']:
                old_zoom = zoom_factor
                zoom_factor *= fast_zoom_speed if move == '9' else slow_zoom_speed
                zoom_point_x = startX + (cursorX / columns) * (3 / old_zoom)
                zoom_point_y = startY + (cursorY / rows) * (2 / old_zoom)
                startX = zoom_point_x - (cursorX / columns) * (3 / zoom_factor)
                startY = zoom_point_y - (cursorY / rows) * (2 / zoom_factor)
            elif move in ['0', ')']:
                old_zoom = zoom_factor
                zoom_factor /= fast_zoom_speed if move == '0' else slow_zoom_speed
                zoom_point_x = startX + (cursorX / columns) * (3 / old_zoom)
                zoom_point_y = startY + (cursorY / rows) * (2 / old_zoom)
                startX = zoom_point_x - (cursorX / columns) * (3 / zoom_factor)
                startY = zoom_point_y - (cursorY / rows) * (2 / zoom_factor)
            pixel_width = 3 / (columns * zoom_factor)
            pixel_height = 2 / (rows * zoom_factor)
            print_board(make_board(columns, rows, pixel_width, pixel_height, startX, startY, cursorX, cursorY))
            columns, rows = os.get_terminal_size()
            if columns != old_columns or rows != old_rows:
                cursorX = (cursorX / old_columns) * columns
                cursorY = (cursorY / old_rows) * rows
                pixel_width = 3 / (columns * zoom_factor)
                pixel_height = 2 / (rows * zoom_factor)
                print_board(make_board(columns, rows, pixel_width, pixel_height, startX, startY, cursorX, cursorY))
        except:
            pass

os.system("cls")
os._exit(1)