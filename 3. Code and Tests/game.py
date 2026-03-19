import curses # For handling user cursor input cleanly
import numpy as np # For generating the board
import scipy # This is for checking for adjacent mines

def run(difficulty):
    def generate_board(board_dimension_preset):
        # Generate a board of the specified size.
        # This is a placeholder for the real board sizes.
        board_dimension_preset = board_dimension_preset * 10
        display_board = np.full((board_dimension_preset, board_dimension_preset), 'x')
        data_board = display_board[np.newaxis(), :] # This is for the data sitting below the board. Mine placements, flags, etc.

        return display_board

    print(generate_board(difficulty)) #Debug purposes only


run(1) #testing purposes only