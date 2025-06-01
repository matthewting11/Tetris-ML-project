import tkinter as tk

root = tk.Tk()
root.title("Blank Window")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="cyan")
canvas.pack()

block_size = 16
cols = 11
rows = 27 
start_x = 200
start_y = 100


def draw_block(x,y,color):
    canvas.create_rectangle(x,y,x+block_size,y+block_size, fill=color, outline="white")
for row in range(rows):
    for col in range(cols):
        x = start_x + col *block_size
        y = start_y + row *block_size
        draw_block(x, y, "black")
score = 0

score_box_x0, score_box_y0 = 20,100
score_box_x1,score_box_y1 = 180,300
canvas.create_rectangle(score_box_x0, score_box_y0, score_box_x1,score_box_y1, outline= "white", width=2)
canvas.create_text((score_box_x0+score_box_x1)/2, score_box_y0 +20, text="Score", fill = "white")
canvas.create_text((score_box_x0 + score_box_x1)/2, score_box_y0 +60, text=score, fill="white", font = ("Courier",24))

next_box_x0, next_box_y0 = 400,100
next_box_x1,next_box_y1 = 550,450

canvas.create_rectangle(next_box_x0, next_box_y0, next_box_x1, next_box_y1, outline= "white", width=2)
canvas.create_text((next_box_x0+next_box_x1)/2, next_box_y0 +20, text="Next", fill = "white")

level_box_x0, level_box_y0 = 20,350
level_box_x1,level_box_y1 = 180,450

level = 1

canvas.create_rectangle(level_box_x0, level_box_y0, level_box_x1, level_box_y1, outline= "white", width=2)
canvas.create_text((level_box_x0+level_box_x1)/2, level_box_y0 +20, text="Level:", fill = "white")
canvas.create_text((level_box_x0 + level_box_x1)/2, level_box_y0 +60, text=level, fill="white", font = ("Courier",24))

root.mainloop()

