import tkinter as tk
import random

root = tk.Tk()
root.title("Tetris Game")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="gray")
canvas.pack()

current_piece = None

def pieceidtoblocks(pieceid):
    if pieceid == 0:
        return [[0,0]]
    elif pieceid == 1:
        return [[0, 0], [1, 0], [0, 1], [1, 1]] #Square
    elif pieceid == 2:
        return [[-1, 0], [0, 0], [1, 0], [2, 0]] #Long
    elif pieceid == 3:
        return [[0, 0], [1, 0], [-1, 1], [0, 1]] #S
    elif pieceid == 4:
        return [[-1, 0], [0, 1], [0, 0], [1, 1]] #Z
    elif pieceid == 5:
        return [[0, 1], [-1, 1], [1, 1], [0, 0]] #T
    elif pieceid == 6:
        return [[-1, 0], [-1, 1], [0, 1], [1, 1]] #L
    elif pieceid == 7:
        return [[-1, 0], [0, 0], [1, 0], [1, 1]] #J
    else:
        return [[]] # FALLBACK CASE, SHOULD NOT HAPPEN
    
block_size = 16
cols = 11
rows = 27 
start_x = 200
start_y = 100



def start_game():
    global paused, start_button, current_piece
    paused = False
    start_button.destroy()
    
    random_piece_id = random.randint(1,7)
    center_col = cols//2
    current_piece = {
    "blocks": [[center_col+ dx, dy] for dx, dy in pieceidtoblocks(random_piece_id)],
    "color": "cyan"
    }


    draw_grid()
    draw_game_UI()
    update_screen()
    update_block()

start_button = tk.Button(root, text="Start Game", font=("Courier", 16), command=start_game)
canvas.create_window(288,316, window=start_button)


paused = False
score = 0
level = 1
block = {"x":5, "y":0}

def draw_block(x,y,color):
    canvas.create_rectangle(x,y,x+block_size,y+block_size, fill=color, outline="white")

def draw_grid():
        for row in range(rows):
            for col in range(cols):
                x = start_x + col *block_size
                y = start_y + row *block_size
                draw_block(x, y, "black")


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

    canvas.create_rectangle(level_box_x0, level_box_y0, level_box_x1, level_box_y1, outline= "white", width=2)
    canvas.create_text((level_box_x0+level_box_x1)/2, level_box_y0 +20, text="Level:", fill = "white")
    canvas.create_text((level_box_x0 + level_box_x1)/2, level_box_y0 +60, text=level, fill="white", font = ("Courier",24))

def update_block():
    if not current_piece or paused:
        root.after(500, update_block)
        return
    if not paused:
        for i in range(len(current_piece["blocks"])):
            current_piece["blocks"][i][1] += 1
        update_screen()
    root.after(500, update_block)


def update_screen():
    canvas.delete("all")
    draw_grid()
    draw_game_UI()
    if not current_piece:
        return
    if current_piece:
        for dx,dy in current_piece["blocks"]:
            x = start_x + dx*block_size
            y = start_y + dy*block_size
            draw_block(x,y,current_piece["color"])

def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        canvas.delete("all")
        canvas.create_rectangle(0,0,576,632, fill="black", stipple="gray25", tags="pause")
        canvas.create_rectangle(138,241,438,391, outline="white", width=3, fill="gray20", tags="pause")
        canvas.create_text(288,316, text="Paused", fill="white", font=("Courier",32),tags="pause")
    else:
        canvas.delete("pause")
        update_screen()


root.bind("<Escape>", toggle_pause)

root.after(500, update_block)

root.mainloop()

