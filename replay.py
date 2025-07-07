import tkinter as tk
import json
import sys

# Import all your game functions and globals
from tetrisml import (
    setup_tetris, piece, update_screen, draw_grid, draw_game_UI, clear_lines, spawn_new_piece
)

root, canvas, board, get_tick_speed = setup_tetris()

# Load moves
filename = sys.argv[1]
with open(filename, "r") as f:
    moves = json.load(f)

# Make sure the board is empty
for r in range(len(board)):
    for c in range(len(board[0])):
        board[r][c] = None

# Speed of replay (ms)
SPEED_MS = 300

current_piece = None

def replay_step(step_index):
    global current_piece

    if step_index >= len(moves):
        print("Replay complete.")
        return

    entry = moves[step_index]
    pieceid = entry["pieceid"]
    rotation = entry["rotation"]
    target_x = entry["x"]

    # Create a new piece
    current_piece = piece(pieceid=pieceid)

    # Rotate piece
    for _ in range(rotation):
        current_piece.cw()

    # Move horizontally to target position
    current_piece.location[0] = target_x

    # Hard drop
    while current_piece.can_move_down(current_piece.blocks):
        current_piece.location[1] += 1

    # Lock the piece into the board
    current_piece.landed = True
    current_piece.fix_piece()

    # Clear any lines
    clear_lines()

    # Redraw
    update_screen()

    # Schedule next step
    root.after(SPEED_MS, lambda: replay_step(step_index + 1))


# Start replay after a short delay
root.after(500, lambda: replay_step(0))

# Start main loop
root.mainloop()
