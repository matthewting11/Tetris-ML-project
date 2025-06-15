import tkinter as tk

root = tk.Tk()
root.title("Blank Window")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="gray")
canvas.pack()

block_size = 16
cols = 11
rows = 27 
start_x = 200
start_y = 100


def draw_block(x,y,color):
    canvas.create_rectangle(x,y,x+block_size,y+block_size, fill=color, outline="white")

def draw_grid():
        for row in range(rows):
            for col in range(cols):
                x = start_x + col *block_size
                y = start_y + row *block_size
                draw_block(x, y, "black")

paused = False
score = 0

def draw_game_UI():
    
    #Score box
    
    score_box_x0, score_box_y0 = 20,100
    score_box_x1,score_box_y1 = 180,300
    canvas.create_rectangle(score_box_x0, score_box_y0, score_box_x1,score_box_y1, outline= "white", width=2)
    canvas.create_text((score_box_x0+score_box_x1)/2, score_box_y0 +20, text="Score", fill = "white")
    canvas.create_text((score_box_x0 + score_box_x1)/2, score_box_y0 +60, text=score, fill="white", font = ("Courier",24))

    #Next box

    next_box_x0, next_box_y0 = 400,100
    next_box_x1,next_box_y1 = 550,450

    canvas.create_rectangle(next_box_x0, next_box_y0, next_box_x1, next_box_y1, outline= "white", width=2)
    canvas.create_text((next_box_x0+next_box_x1)/2, next_box_y0 +20, text="Next", fill = "white")

    #level box

    level_box_x0, level_box_y0 = 20,350
    level_box_x1,level_box_y1 = 180,450

    level = 1

    canvas.create_rectangle(level_box_x0, level_box_y0, level_box_x1, level_box_y1, outline= "white", width=2)
    canvas.create_text((level_box_x0+level_box_x1)/2, level_box_y0 +20, text="Level:", fill = "white")
    canvas.create_text((level_box_x0 + level_box_x1)/2, level_box_y0 +60, text=level, fill="white", font = ("Courier",24))

def draw_pause_overlay():
    canvas.create_rectangle(0,0,576,632, fill="black", stipple="gray25", tags="pause")
    canvas.create_rectangle(138,241,438,391, outline="white", width=3, fill="gray20", tags="pause")
    canvas.create_text(288,316, text="Paused", fill="white", font=("Courier",32),tags="pause")

def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
          canvas.delete("all")
          draw_pause_overlay()
    else:
        canvas.delete("all")
        draw_grid()
        draw_game_UI()

root.bind("<Escape>", toggle_pause)

draw_grid()
draw_game_UI()

root.mainloop()

