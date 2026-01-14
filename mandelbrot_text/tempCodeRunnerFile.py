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