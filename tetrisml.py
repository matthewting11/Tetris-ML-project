import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Tetris Game")
root.geometry("576x632")

canvas = tk.Canvas(root, width=576, height=632, bg="black")
canvas.pack()

board = [[None for _ in range(11)] for _ in range(27)]

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
        return [[1, 0], [-1, 1], [0, 1], [1, 1]] #L
    elif pieceid == 7:
        return [[-1, 0], [0, 0], [1, 0], [1, 1]] #J
    else:
        return [[]] # FALLBACK CASE, SHOULD NOT HAPPEN
def piece_color(pieceid):
    colors = {
        0: "lightgray",
        1: "yellow",
        2: "cyan",
        3: "red",
        4: "lightgreen",
        5: "purple",
        6: "orange",
        7: "lightblue"
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
        self.landed = False
        self.color = piece_color(pieceid)
        self.blocks = pieceidtoblocks(pieceid)
        self.pivot = center_piece(pieceid)
        self.location = [5,0]
        self.lock_time = 0
    
    def can_move_left(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            boundy = y + self.location[1]
            if boundx<=0 or board[int(boundy)][int(boundx-1)] is not None:
                return False
        return True
    def can_move_right(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            boundy = y + self.location[1]
            if boundx>=10 or board[int(boundy)][int(boundx+1)] is not None:
                return False
        return True
    def can_rotate(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            boundy = y + self.location[1]
            if boundx>=11 or boundx<=-1 or boundy>=26:
                return False
        return True
    def can_move_down(self,new_blocks):
        for x,y in new_blocks:
            absx = int(x+self.location[0])
            absy= int(y + self.location[1])
            if absy>=26 or board[int(absy)+1][int(absx)] is not None:
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
    def soft(self):
        #softdrop block down a space (hold to drop faster):
        for x,y in self.blocks:
            new_blocks = []
        for block in self.blocks:
            x,y = block
            new_y = y
            new_blocks.append([x,new_y])
        if self.can_move_down(new_blocks):
            self.blocks = new_blocks
            self.location[1] += 1
            return self.blocks
        else:
            return self.blocks
    def hard(self):
        global points_added, score
        #harddrop block on lowest possible level:
        if paused or current_piece is None:
            return
        for x,y in self.blocks:
            new_blocks = []
        for block in self.blocks:
            x,y = block
            new_y = y
            new_blocks.append([x,new_y])
        while current_piece.can_move_down(new_blocks):
            current_piece.blocks = new_blocks
            current_piece.location[1]+=1
        current_piece.landed = True
        current_piece.fix_piece()
        clear_lines()
        score += points_added
        root.after(100,update_block)
        spawn_new_piece()
        update_screen()
        
    def fix_piece(self):
        offset_x, offset_y = self.location  # piece's position on the grid
        for dx, dy in self.blocks:
            col = int(dx + offset_x)
            row = int(dy + offset_y)
            if 0 <= row < rows and 0 <= col < cols:
                board[row][col] = self.color
        


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
running = True
def start_game():
    global paused, start_button,current_piece, board
    paused = False
    start_button.destroy()
    
    random_piece_id = random.randint(1,7)
    current_piece = piece(pieceid=random_piece_id)
    
    draw_grid()
    draw_game_UI()    
    update_screen()
    update_block()

    
controls = [
    "← / → arrow keys : Move L/R",
    "↓ arrow key : Soft Drop",
    "Space-bar : Hard drop",
    "↑ : Rotate CW",
    "Z : Rotate CCW",
    "Esc : Pause"
   ]    
for i, line in enumerate(controls):
    canvas.create_text(288, 300 + i*20, text=line, fill="white", font=("Courier",12),tags="Pause")

start_button = tk.Button(root, text="▶ Start Game",cursor="hand2", font=("Courier", 16), bg="#444444",fg="white",relief="raised",command=start_game)
canvas.create_window(288,150, window=start_button)

paused = False
score = 0
level = 1
block = {"x":5, "y":0}

#SETTING UI

def draw_block(x,y,color):
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")

def draw_grid():
        for row in range(-1,rows):
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
    global current_piece, board, score
    if not paused:
        new_blocks = []
        for block in current_piece.blocks:
            x,y = block
            new_blocks.append([x,y])

        if current_piece.can_move_down(new_blocks)== True:
            current_piece.blocks = new_blocks
            current_piece.location[1] += 1
            update_screen()
            root.after(tick_speed, update_block)
            current_piece.lock_time = 0
        
        elif current_piece.can_move_down(new_blocks) == False :
            
            print("cant move")
            
            if current_piece.lock_time == 0:
                current_piece.lock_time = time.time()
                print("fixing")
            
            elif float(time.time()) - float(current_piece.lock_time) >= 0.5:
                current_piece.landed = True
                print("fixed")
                current_piece.fix_piece()
                clear_lines()
                score+=points_added
                spawn_new_piece()
            root.after(100,update_block)
            print(float(time.time()) - float(current_piece.lock_time))
            
    else:
        print("lol")
        return

def spawn_new_piece():
    global current_piece
    random_piece_id = 2#(random.randint(1,7)
    current_piece = piece(pieceid = random_piece_id)
    update_screen()

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
    #Marked pivot point
    '''
    canvas.create_oval(
        px - radius, py - radius,
        px + radius, py + radius,
        fill="yellow", outline=""
    )
    '''

def clear_lines():
    global board
    global points_added
    print("clearing lines")
    new_board = []
    for row in board:
        full = True
        for cell in row:
            if cell is None:
                full = False
                break
        if not full:
            new_board.append(row)
    lines_cleared = rows - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0,[None for _ in range(cols)])
    board = new_board
    print("cleared",lines_cleared)
    points_added = 0
    if lines_cleared == 1:
        points_added = 40
    elif lines_cleared == 2:
        points_added = 100
    elif lines_cleared == 3:
        points_added = 300
    elif lines_cleared == 4:
        points_added = 1200
    return points_added

def update_screen():
    canvas.delete("all")
    draw_grid()
    draw_game_UI()
    for row in range(rows):
        for col in range(cols):
            color = board[row][col]
            if color:
                x = start_x + col * block_size
                y = start_y + row * block_size
                draw_block(x,y,color)
    if current_piece:
        draw_piece()


# SETUP PAUSE SYSTEM
def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        canvas.delete("all")
        canvas.create_rectangle(0,0,576,632, fill="black", stipple="gray25", tags="pause")
        canvas.create_rectangle(138,241,438,391, outline="white", width=3, fill="gray20", tags="pause")
        canvas.create_text(288,316, text="Paused", fill="white", font=("Courier",32),tags="pause")

        controls = [
            "← / → arrow keys : Move L/R",
            "↓ arrow key : Soft Drop",
            "Space-bar : Hard drop",
            "↑ : Rotate CW",
            "Z : Rotate CCW",
            "Esc : Pause"
        ]
        for i, line in enumerate(controls):
            canvas.create_text(288, 400 + i*20, text=line, fill="lightgray", font=("Courier",12),tags="Pause")

    else:
        canvas.delete("pause")
        update_screen()
# CONTROLS MENU
def draw_controls_menu(screen, font, title= "Controls"):
    screen.fill

#SETTING UP MOVEMENT FUNCTION
def rotate_piece_CCW(event=None):
    if not paused and current_piece:
        current_piece.ccw()
        current_piece.lock_time = 0
        update_screen()
def rotate_piece_CW(event=None):
    if not paused and current_piece:
        current_piece.cw()
        current_piece.lock_time = 0
        update_screen()
def moveblock_L(self):
    if not paused and current_piece:
        current_piece.l()
        current_piece.lock_time = 0
        update_screen()
def moveblock_R(self):
    if not paused and current_piece:
        current_piece.r()
        current_piece.lock_time = 0
        update_screen()
def softdrop(self):
    if not paused and current_piece:
        current_piece.soft()
        current_piece.lock_time = 0
        update_screen()
def harddrop(self):
    if not paused and current_piece:
        current_piece.hard()
        current_piece.lock_time = 0
        update_screen()




root.bind("<Escape>", toggle_pause)
root.bind("<z>",rotate_piece_CCW)
root.bind("<Up>",rotate_piece_CW)
root.bind("<Left>",moveblock_L)
root.bind("<Right>",moveblock_R)
root.bind("<Down>",softdrop)
root.bind("<space>",harddrop)



root.mainloop()

