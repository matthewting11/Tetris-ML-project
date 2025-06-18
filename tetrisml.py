import tkinter as tk
import random

root = tk.Tk()
root.title("Tetris Game")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="gray")
canvas.pack()



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
def piece_color(pieceid):
    colors = {
        0: "gray",
        1: "yellow",
        2: "cyan",
        3: "red",
        4: "green",
        5: "purple",
        6: "orange",
        7: "blue"
    }
    return colors.get(pieceid,"gray")
#DEFINE ROTATION AXIS
def center_piece(pieceid):
    # Define the pivot for each piece.
    # (These are one acceptable set of pivot points for classic Tetris.)
    if pieceid == 1:   # O-tetromino
        pivot = (0.5, 0.5)
    elif pieceid == 2:  # I-tetromino
        pivot = (1.5, 0.5)
    elif pieceid in (3, 4, 5):  # S, Z, T
        pivot = (0, 1)
    elif pieceid == 6:  # L (or mirror; note: some implementations may choose a different pivot)
        pivot = (0, 1)
    elif pieceid == 7:
        pivot = (0,0)
    elif pieceid == 0:  
        pivot = (0, 0)
    else:
        raise ValueError("Unknown piece")
    
    # Return the pivot point as a tuple (x, y). 
    return pivot




#DEFINING CLASSES
class piece:
    def __init__(self, pieceid=0, landed=0):
        self.pieceid = pieceid
        self.landed = landed
        self.color = piece_color(pieceid)
        self.blocks = pieceidtoblocks(pieceid)
        self.pivot = center_piece(pieceid)
        self.location = [5,0]
    
    def can_move_left(self,new_blocks):
        print(new_blocks)
        for x,y in new_blocks:
            boundx = x + self.location[0]
            if boundx<=0:
                return False
        return True
    def can_move_right(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            if boundx>=10:
                return False
        return True
    def can_rotate(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            if boundx>=11 or boundx<=-1:
                return False
        return True

    def ccw(self):
        # Rotate the piece counter-clockwise
         # Please pass in the whatever "rotated_blocks" is because it's missing an argument 
        new_blocks = []
        for block in self.blocks:
            x, y = block
            new_x = y - self.pivot[1] + self.pivot[0]
            new_y = -x + self.pivot[0] + self.pivot[1]
            new_blocks.append([new_x, new_y])
            
        if self.can_rotate(new_blocks):
            self.blocks = new_blocks
            return new_blocks
        else:
            return self.blocks
    def cw(self):
        # Rotate the piece clockwise
        new_blocks = []
        for block in self.blocks:
            x, y = block
            new_x = -y + self.pivot[0] + self.pivot[1]
            new_y = x - self.pivot[0] + self.pivot[1]
            new_blocks.append([new_x, new_y])
            print(new_blocks)
        if self.can_rotate(new_blocks):
            self.blocks = new_blocks
            return self.blocks
        else:
            return self.blocks

    def l(self):
        #Move blocks left
        new_blocks = []
        for block in self.blocks:
            x,y = block
            new_x = x
            new_blocks.append([new_x,y])
        if self.can_move_left(new_blocks):
            self.blocks = new_blocks
            self.location[0] -= 1
            return self.blocks
        else:
            return self.blocks


    def r(self):
        #Move blocks right
        for x,y in self.blocks:
            if x+1 >= 4:
                return
        new_blocks = []
        for block in self.blocks:
            x,y = block
            new_x = x
            new_blocks.append([new_x,y])
        if self.can_move_right(new_blocks):    
            self.blocks = new_blocks
            self.location[0] += 1
            return self.blocks
        else:
            return self.blocks


block_size = 16
cols = 11
rows = 27 
start_x = 200
start_y = 100
tick_speed = 800

#DEFINE BORDERS
left_bound = -cols // 2
right_bound = cols // 2
bottom_bound = 84

#STARTING GAME

def start_game():
    global paused, start_button,current_piece
    paused = False
    start_button.destroy()
    
    random_piece_id = random.randint(1,7)
    current_piece = piece(pieceid=random_piece_id)
    
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

#SETTING UI

def draw_block(x,y,color):
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")

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

#SETTING BLOCK TICK MOVEMENT

def update_block():
    if not current_piece or paused:
        root.after(tick_speed, update_block)
        return

    current_piece.location[1] += 1
    update_screen()
    root.after(tick_speed, update_block)

def draw_piece():
    for dx,dy in current_piece.blocks:
        x = start_x + (current_piece.location[0]+dx)*block_size
        y = start_y + (current_piece.location[1]+dy)*block_size
        draw_block(x,y,current_piece.color)
    # Draw pivot point as a small yellow circle
    pivot_x = current_piece.location[0] + current_piece.pivot[0]
    pivot_y = current_piece.location[1] + current_piece.pivot[1]

    # Convert grid coordinates to pixel
    px = start_x + pivot_x * block_size
    py = start_y + pivot_y * block_size
    radius = block_size // 4
    canvas.create_oval(
        px - radius, py - radius,
        px + radius, py + radius,
        fill="yellow", outline=""
    )
def update_screen():
    canvas.delete("all")
    draw_grid()
    draw_game_UI()
    if not current_piece:
        return
    if current_piece:
        draw_piece()
        print("location at",current_piece.location)


# SETUP PAUSE SYSTEM
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

#SETTING UP MOVEMENT FUNCTION
def rotate_piece_CCW(event=None):
    if not paused and current_piece:
        current_piece.ccw()
        update_screen()
def rotate_piece_CW(event=None):
    if not paused and current_piece:
        current_piece.cw()
        update_screen()
def moveblock_L(self):
    if not paused and current_piece:
        current_piece.l()
        update_screen()
def moveblock_R(self):
    if not paused and current_piece:
        current_piece.r()
        update_screen()




root.bind("<Escape>", toggle_pause)
root.bind("<z>",rotate_piece_CCW)
root.bind("<Up>",rotate_piece_CW)
root.bind("<Left>",moveblock_L)
root.bind("<Right>",moveblock_R)



root.mainloop()

