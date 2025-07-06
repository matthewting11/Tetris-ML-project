import tkinter as tk
import time
import json
import sys
import random

from tetrisml import *

# Load moves file from argument
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

# Start the first piece
current_piece = piece(pieceid=random.randint(1,7))

def apply_move(move):
    if move == "left":
        current_piece.l()
    elif move == "right":
        current_piece.r()
    elif move == "rotate":
        current_piece.cw()
    elif move == "drop":
        current_piece.hard()
    elif move == "nothing":
        pass

def replay_step(step_index):
    if step_index >= len(moves):
        print("Replay complete.")
        return
    move = moves[step_index]
    apply_move(move)
    update_screen()
    root.after(300, lambda: replay_step(step_index+1))

start_game()
root.after(1000, lambda: replay_step(0))
root.mainloop()
