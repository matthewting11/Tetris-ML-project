import tkinter as tk

root = tk.Tk()
root.title("Blank Window")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="black")
canvas.pack()

block_size = 16
cols = 576 // block_size
rows = 632 // block_size

def draw_block(x,y,color):
    canvas.create_rectangle(x,y,x+block_size,y+block_size, fill=color, outline="white")
for row in range(rows):
    for col in range(cols):
        color = "gray"
        draw_block(col * block_size, row * block_size, color)

root.mainloop()