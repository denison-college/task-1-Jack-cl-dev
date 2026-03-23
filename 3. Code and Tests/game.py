import curses # For handling user cursor input cleanly
import numpy as np # For generating the board
import scipy # This is for checking for adjacent mines

difficulty_size = { #This is a simple dictionary for the difficulty levels, to make changing it easier during development.
    1: 10,
    2: 40,
    3: 99,
}
difficulty_mines = {
    1: 10,
    2: 40,
    3: 99,
}

def run(difficulty):
    #TODO: Call these functions, with code to parse difficulty_mines into place_mines and difficulty_size into generate_board.
    def generate_board(board_dimension_preset): #TODO Replace board dimension preset with difficulty_size[difficulty] implementation
        """
        This function is *not* used to print the game board. It is used to generate the board data,
        from which the game board is generated.
        """
        # Generate a board of the specified size.
        # This is a placeholder for the real board sizes.
        board_dimension_preset = board_dimension_preset * 10
        display_board = np.full((board_dimension_preset, board_dimension_preset), 'x')
        data_board = display_board[np.newaxis(), :] # This is for the data sitting below the board. Mine placements, flags, etc.
        def place_mines(data_board, num_mines):
            """Randomly place mines on the data board. Requires Data_board and number of mines."""
            rows, cols = data_board.shape
            total_tiles = rows * cols

            # Pick unique random positions (flat indices)
            mine_indices = np.random.choice(total_tiles, size=num_mines, replace=False)

            # Convert flat indices to 2D coordinates
            mine_positions = np.unravel_index(mine_indices, (rows, cols))

            # Place mines (using 'M' or any marker you prefer)
            data_board[mine_positions] = 'M'

            return data_board
        place_mines(data_board, difficulty_mines[difficulty])
        return display_board
    def display_board(stdscr, board, cursor_pos=(0, 0)):
        """Render the board using curses with a highlighted cursor position."""
        stdscr.clear()
        rows, cols = board.shape

        # Draw column headers
        header = "   " + " ".join(f"{i:2}" for i in range(cols))
        stdscr.addstr(0, 0, header)
        stdscr.addstr(1, 0, "   " + "---" * cols)

        # Draw each row
        for row_idx in range(rows):
            stdscr.addstr(row_idx + 2, 0, f"{row_idx:2} |")
            for col_idx in range(cols):
                cell = board[row_idx, col_idx]
                x_pos = 4 + col_idx * 3
                y_pos = row_idx + 2

                # Highlight cursor position
                if (row_idx, col_idx) == cursor_pos:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y_pos, x_pos, f"{cell:2}")
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y_pos, x_pos, f"{cell:2}")

        stdscr.refresh()

    generate_board(difficulty_size[difficulty])
    display_board(generate_board(difficulty_size[difficulty]))

    def game_loop(stdscr): #TODO: review this function.
        board = generate_board(difficulty_size[difficulty])
        cursor_pos = (0, 0)

        while True:
            display_board(stdscr, board, cursor_pos)
            key = stdscr.getch()

            # Handle arrow keys to move cursor
            if key == curses.KEY_UP and cursor_pos[0] > 0:
                cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
            elif key == curses.KEY_DOWN and cursor_pos[0] < board.shape[0] - 1:
                cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
            elif key == curses.KEY_LEFT and cursor_pos[1] > 0:
                cursor_pos = (cursor_pos[0], cursor_pos[1] - 1)
            elif key == curses.KEY_RIGHT and cursor_pos[1] < board.shape[1] - 1:
                cursor_pos = (cursor_pos[0], cursor_pos[1] + 1)
            elif key == ord('q'):
                break

    curses.wrapper(game_loop)

    game_loop()
run(1)