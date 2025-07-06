import tkinter as tk
import json
import sys

from tetrisml import *

# Load moves file
filename = sys.argv[1]

with open(filename, "r") as f:
    moves = json.load(f)

root = tk.Tk()
root.title("Tetris Replay")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="black")
canvas.pack()

# Re-initialize board
board = [[None for _ in range(11)] for _ in range(29)]

# Settings
SPEED_MS = 100

def replay_step(step_index):
    global current_piece
    if step_index >= len(moves):
        print("Replay complete.")
        return

    entry = moves[step_index]
    pieceid = entry["pieceid"]
    rotation = entry["rotation"]
    target_x = entry["x"]

    # Create the piece
    current_piece = piece(pieceid=pieceid)

    # Rotate it
    for _ in range(rotation):
        current_piece.cw()

    # Move horizontally to the target position
    current_piece.location[0] = target_x

    # Hard drop
    current_piece.hard()

    # Redraw the screen
    update_screen()

    # Wait for the next step
    root.after(SPEED_MS, lambda: replay_step(step_index + 1))

# Start game to initialize
start_game()

# Begin replay after a short delay
root.after(500, lambda: replay_step(0))

root.mainloop()
