import curses
import numpy as np
import time
#On Windows, this project needs to be run with the windows-curses package installed. Not sure how to package this with the EXE.

# Dictionary for short variable names used throughout this file:
# r      = row index (current cell)
# c      = column index (current cell)
# dr     = delta row (offset for neighbour checking: -1, 0, or 1)
# dc     = delta column (offset for neighbour checking: -1, 0, or 1)
# fr     = first click row
# fc     = first click column
# nr     = neighbour row (r + dr)
# nc     = neighbour column (c + dc)
# h      = height (terminal window)
# w      = width (terminal window)
# fg     = foreground colour
# bg     = background colour
# stdscr = standard screen (curses main window object)
# attr   = attribute (curses text formatting/colour)
# ui     = user input

difficulty_size = {
    1: (9, 9),
    2: (16, 16),
    3: (16, 30),
}
difficulty_mines = {
    1: 10,
    2: 40,
    3: 99,
}
def run(difficulty, settings, colours):
    def generate_board(board_dimension_preset):
        """
        Generate the board data used by the game.
        Initially, the board is empty. Mines are placed after the first click.
        """
        rows, cols = board_dimension_preset
        data_board = np.full((rows, cols), ' ', dtype=object)
        display_board_child = np.full((rows, cols), 'x', dtype=object)

        return data_board, display_board_child
    def place_mines(data_board_child, num_mines, first_click_pos):
        rows, cols = data_board_child.shape
        total_tiles = rows * cols

        # Ensure the first click and its neighbours are not mines.
        blocked_indices = []
        fr, fc = first_click_pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = fr + dr, fc + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    blocked_indices.append(nr * cols + nc)

        available_indices = [i for i in range(total_tiles) if i not in blocked_indices]
        
        # If there are not enough available tiles, just exclude the first click itself
        if len(available_indices) < num_mines:
            available_indices = [i for i in range(total_tiles) if i != fr * cols + fc]

        mine_indices = np.random.choice(available_indices, size=num_mines, replace=False)
        mine_positions = np.unravel_index(mine_indices, (rows, cols))
        data_board_child[mine_positions] = 'M'

        # Pre-calculate adjacent mine counts for each cell
        for r in range(rows):
            for c in range(cols):
                if data_board_child[r, c] == 'M':
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if data_board_child[nr, nc] == 'M':
                                count += 1
                data_board_child[r, c] = str(count) if count > 0 else ' '

        return data_board_child
    def display_board(stdscr, board, cursor_pos=(0, 0), flags_placed=0, time_elapsed=0):
        stdscr.clear()
        rows, cols = board.shape
        max_y, max_x = stdscr.getmaxyx() #Max X and Y of the terminal window

        total_mines = difficulty_mines[difficulty]
        mine_info = f" Flags: {flags_placed}/{total_mines} | Time: {int(time_elapsed)}s"
        help_info = " Arrows: Move | Enter: Reveal | F: Flag | Q: Quit"
        header = "   " + " ".join(f"{i:2}" for i in range(cols))
        separator = "   " + "---" * cols

        # Prevent curses from drawing beyond the terminal window (or at least tries, anyhow), which crashes the entire script (for some reason)
        if 0 < max_y:
            stdscr.addstr(0, 0, header[: max_x - 1])
        if 1 < max_y:
            stdscr.addstr(1, 0, separator[: max_x - 1])
        
        # Display mine/flag info and help if there's space
        if 0 < max_y:
            info_attr = curses.color_pair(11) # Colour for mine_count from settings
            stdscr.addstr(0, max_x - len(mine_info) - 1 if max_x > len(mine_info) else 0, mine_info, info_attr)
            
            # Display help text in the second row (if there's space on the right)
            if max_x > len(help_info) + len(separator):
                 stdscr.addstr(1, max_x - len(help_info) - 1, help_info)
            elif max_y > rows + 2: # Or below the board
                 stdscr.addstr(rows + 2, 0, help_info[:max_x-1])

        for row in range(rows): #Draw each row
            y_pos = row + 2
            if y_pos >= max_y:
                break

            row_label = f"{row:2} |"
            stdscr.addstr(y_pos, 0, row_label[: max_x - 1])

            for col_idx in range(cols): #Draw each column
                x_pos = 4 + col_idx * 3
                cell_value = board[row, col_idx]
                
                # Use symbols from settings
                if cell_value == 'F':
                    display_char = settings["flag_symbol"]
                elif cell_value == 'M':
                    display_char = settings["mine symbol"]
                else:
                    display_char = cell_value
                
                cell_text = f"{display_char:2}"

                if x_pos + len(cell_text) >= max_x:
                    break

                attr = curses.A_NORMAL
                if cell_value == 'F':
                    attr = curses.color_pair(9)
                elif cell_value == 'M':
                    attr = curses.color_pair(10)
                elif cell_value in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    attr = curses.color_pair(int(cell_value))

                if (row, col_idx) == cursor_pos: #Highlight the cursor position
                    attr |= curses.A_REVERSE
                
                stdscr.addstr(y_pos, x_pos, cell_text, attr)

        stdscr.refresh()
    def game_loop(stdscr): #Seriously, could they not come up with something easier than stdscr?
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.nodelay(True)
        curses.start_color()
        
        # Initialize colours
        colour_map = {
            "black": curses.COLOR_BLACK,
            "white": curses.COLOR_WHITE,
            "red": curses.COLOR_RED,
            "green": curses.COLOR_GREEN,
            "yellow": curses.COLOR_YELLOW,
            "blue": curses.COLOR_BLUE,
            "magenta": curses.COLOR_MAGENTA,
            "cyan": curses.COLOR_CYAN,
            "1": curses.COLOR_CYAN,
            "2": curses.COLOR_GREEN,
            "3": curses.COLOR_RED,
            "4": curses.COLOR_BLUE,
            "5": curses.COLOR_YELLOW,
            "6": curses.COLOR_MAGENTA,
            "7": curses.COLOR_CYAN,
            "8": curses.COLOR_BLACK,
        }

        # Background and Text
        bg = colour_map.get(colours.get("background", "black"), curses.COLOR_BLACK)
        
        # Colour pairs for numbers 1-8
        for i in range(1, 9):
            fg = colour_map.get(colours.get(str(i), "white"), curses.COLOR_WHITE)
            curses.init_pair(i, fg, bg)
        
        # Colour pairs for the flag and the mine
        curses.init_pair(9, colour_map.get(colours.get("flag", "red"), curses.COLOR_RED), bg)
        curses.init_pair(10, colour_map.get(colours.get("mine", "green"), curses.COLOR_GREEN), bg)
        curses.init_pair(11, colour_map.get(colours.get("mine_count", "blue"), curses.COLOR_BLUE), bg)

        data_board, visible_board = generate_board(difficulty_size[difficulty])
        cursor_pos = (0, 0)
        game_over = False
        mines_placed = False
        start_time = None
        final_time = 0
        message = ""
        total_mines = difficulty_mines[difficulty]

        def reveal_tile(r, c): #Row and column if you don't remember.
            if visible_board[r, c] != 'x':
                return
            
            visible_board[r, c] = data_board[r, c]
            
            if data_board[r, c] == ' ':
                rows, cols = data_board.shape
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            reveal_tile(nr, nc)

        while True:
            current_time = time.time()
            time_elapsed = current_time - start_time if start_time else final_time
            
            flags_placed = np.count_nonzero(visible_board == 'F')
            display_board(stdscr, visible_board, cursor_pos, flags_placed, time_elapsed) #Python isn't happy about flags_placed, because np outputs some freak of an integer, *but* the code works. So, I'm not fixing it.
            if message:
                stdscr.addstr(data_board.shape[0] + 3, 0, message)
                stdscr.refresh()

            if game_over:
                # Re-display the board once more with the final state
                display_board(stdscr, visible_board, cursor_pos, flags_placed, final_time)
                
                # Create a simple message box at the centre/bottom
                h, w = stdscr.getmaxyx()
                msg_win = curses.newwin(5, len(message) + 4, h // 2 - 2, (w - len(message) - 4) // 2)
                msg_win.box()
                msg_win.addstr(2, 2, message)
                msg_win.refresh()
                
                stdscr.nodelay(False)
                stdscr.getch()
                break

            key = stdscr.getch()
            if key == -1: # No key pressed
                time.sleep(0.05)
                continue

            if key == curses.KEY_UP and cursor_pos[0] > 0:
                cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
            elif key == curses.KEY_DOWN and cursor_pos[0] < data_board.shape[0] - 1:
                cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
            elif key == curses.KEY_LEFT and cursor_pos[1] > 0:
                cursor_pos = (cursor_pos[0], cursor_pos[1] - 1)
            elif key == curses.KEY_RIGHT and cursor_pos[1] < data_board.shape[1] - 1:
                cursor_pos = (cursor_pos[0], cursor_pos[1] + 1)
            elif key in [curses.KEY_ENTER, 10, 13]:
                r, c = cursor_pos
                if not mines_placed:
                    place_mines(data_board, total_mines, (r, c))
                    mines_placed = True
                    start_time = time.time()

                if visible_board[r, c] == 'x':
                    if data_board[r, c] == 'M':
                        # Reveal all mines
                        mine_positions = np.where(data_board == 'M')
                        visible_board[mine_positions] = 'M'
                        game_over = True
                        final_time = time.time() - start_time
                        start_time = None
                        message = " Game Over! You hit a mine. Press any key to exit. "
                    else:
                        reveal_tile(r, c)
                        #Check win condition: if only mines are left hidden/flagged
                        hidden_count = np.count_nonzero(visible_board == 'x') + np.count_nonzero(visible_board == 'F')
                        if hidden_count == total_mines:
                            game_over = True
                            final_time = time.time() - start_time
                            start_time = None
                            message = f" You Win! All mines cleared in {int(final_time)}s. Press any key to exit. "
                elif visible_board[r, c].isdigit():
                    num = int(visible_board[r, c])
                    adjacent_flags = 0
                    rows, cols = data_board.shape
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if visible_board[nr, nc] == 'F':
                                    adjacent_flags += 1
                    #I'm going to have an aneurysm, this might be the least readable thing I've ever written.
                    if adjacent_flags == num:
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0: continue
                                nr, nc = r + dr, c + dc
                                if 0 <= nr < rows and 0 <= nc < cols:
                                    if visible_board[nr, nc] == 'x':
                                        if data_board[nr, nc] == 'M':
                                            #Hit a mine
                                            mine_positions = np.where(data_board == 'M')
                                            visible_board[mine_positions] = 'M'
                                            game_over = True
                                            final_time = time.time() - start_time
                                            start_time = None
                                            message = " Game Over! Press any key to exit. "
                                        else:
                                            reveal_tile(nr, nc)
                        
                        #Check win condition
                        hidden_count = np.count_nonzero(visible_board == 'x') + np.count_nonzero(visible_board == 'F')
                        if not game_over and hidden_count == total_mines:
                            game_over = True
                            final_time = time.time() - start_time
                            start_time = None
                            message = f" You Win! All mines cleared in {int(final_time)}s. Press any key to exit. "

            elif key == ord('f'):
                if not mines_placed: #Don't allow flags before the first click
                    continue
                r, c = cursor_pos
                if visible_board[r, c] == 'x':
                    if flags_placed < total_mines:
                        visible_board[r, c] = 'F'
                elif visible_board[r, c] == 'F':
                    visible_board[r, c] = 'x'
            elif key == ord('q'):
                break

    curses.wrapper(game_loop)