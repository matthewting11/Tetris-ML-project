import tkinter as tk
import random
import time
root = tk.Tk()


def pieceidtoblocks(pieceid):
    #Sets coordinates of tiles to relative block locations to create a unique piece
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


"""
DOCUMENTATION BECAUSE WE ARE NOT ANIMALS

MAIN Loop:
1. Initialize the game board and UI.
2. Create a new piece and draw the grid.
3. Handle user input for piece movement and rotation.
4. Update the piece position based on user input and game logic.
5. Check for line clears and update the score.
6. Redraw the game board and pieces.
7. Repeat the loop until the game is over or paused.

The functions called in the main loop are:
- `start_game()`: Initializes the game, spawns the first piece, and sets up the UI.
- `draw_grid()`: Draws the game grid on the canvas.

Main Loop:
- `draw_game_UI()`: Draws the score, lines cleared, next piece, and level information on the canvas.    
- `update_block()`: Updates the position of the current piece based on game logic and user input.

- `draw_piece()`: Draws the current piece on the canvas.
- `clear_lines()`: Checks for full lines, clears them, updates the score, and adjusts the game level.
-
`update_screen()`: Redraws the entire game screen, including the grid, pieces, and UI elements.
    Calls   `draw_grid()`
            `draw_game_UI()`
            `draw_piece()` 




"""

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
    
    def game_over_check(self):
        if self.landed:
            for x,y in self.blocks:
                if y + self.location[1] <= 4:
                    return True
        return False

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
            if boundx>=11 or boundx<=-1 or boundy>=26 or board[int(boundy)][int(boundx)] is not None:
                return False
        return True
    def can_move_down(self,new_blocks):
        global score, points_added
        for x,y in new_blocks:
            absx = int(x+self.location[0])
            absy = int(y+self.location[1])
            if absy>=25 or board[int(absy)+1][int(absx)] is not None:
                if current_piece.game_over_check():  # Check if the game is over
                    draw_game_over()
                    running = False
                    return  # Exit without spawning a new piece
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
            if current_piece.game_over_check():  # Check if the game is over
                draw_game_over()
                running = False
                return
            

    def hard(self):
        global points_added, score, gameover
        #harddrop block on lowest possible level:
        if paused or gameover or current_piece is None:
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
        if current_piece.game_over_check():  # Check if the game is over
            gameover = True
            draw_game_over()
            return  # Exit without spawning a new piece
        current_piece.fix_piece()
        clear_lines()
        score += points_added
        update_screen()
        spawn_new_piece()

    def fix_piece(self):
        offset_x, offset_y = self.location  # piece's position on the grid
        for dx, dy in self.blocks:
            col = int(dx + offset_x)
            row = int(dy + offset_y)
            if 0 <= row < rows and 0 <= col < cols:
                board[row][col] = self.color
        update_screen()
    

def start_game():
    global paused, start_button,current_piece, board, gameover
    paused = False
    gameover = False
    start_button.destroy()

    canvas.delete("all")
    

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
tetris_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
tetris_letters = "TETRIS"
startingx = 100  # Starting x position
y = 150         # y position for all letters

for i, letter in enumerate(tetris_letters):
    canvas.create_text(
        startingx + i * 80,  # Adjust spacing between letters
        y,
        text=letter,
        fill=tetris_colors[i],
        font=("Courier", 100, "bold"),
        tags="start"
    )
start_button = tk.Button(root, text="▶ Start Game",cursor="hand2", font=("Courier", 16), bg="#444444",fg="white",relief="raised",command=start_game)
canvas.create_window(288,250, window=start_button, tags="start")
canvas.pack()




#SETTING UI

def draw_block(x,y,color):
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")

def draw_grid():
        for row in range(-2,rows):
            for col in range(cols):
                x = start_x + col *block_size
                y = start_y + row *block_size
                draw_block(x, y, "black")


def draw_game_UI():
    global total_lines_cleared,score,level
    #Score box
    
    score_box_x0, score_box_y0 = 20, 100
    score_box_x1, score_box_y1 = 180, 300

    canvas.create_rectangle(score_box_x0, score_box_y0, score_box_x1, score_box_y1, outline="white", width=2)
    canvas.create_text((score_box_x0 + score_box_x1) / 2, score_box_y0 + 20, text="Score", fill="white")
    canvas.create_text((score_box_x0 + score_box_x1) / 2, score_box_y0 + 60, text=score, fill="white", font=("Courier", 24))

    # Lines cleared
    canvas.create_text((score_box_x0 + score_box_x1) / 2, score_box_y0 + 120, text="Lines", fill="white")
    canvas.create_text((score_box_x0 + score_box_x1) / 2, score_box_y0 + 160, text=total_lines_cleared, fill="white", font=("Courier", 24))

    # Next box
    next_box_x0, next_box_y0 = 400, 100
    next_box_x1, next_box_y1 = 550, 450

    canvas.create_rectangle(next_box_x0, next_box_y0, next_box_x1, next_box_y1, outline="white", width=2)
    canvas.create_text((next_box_x0 + next_box_x1) / 2, next_box_y0 + 20, text="Next", fill="white")

    # Level box
    level_box_x0, level_box_y0 = 20, 350
    level_box_x1, level_box_y1 = 180, 450

    canvas.create_rectangle(level_box_x0, level_box_y0, level_box_x1, level_box_y1, outline="white", width=2)
    canvas.create_text((level_box_x0 + level_box_x1) / 2, level_box_y0 + 20, text="Level:", fill="white")
    canvas.create_text((level_box_x0 + level_box_x1) / 2, level_box_y0 + 60, text=level, fill="white", font=("Courier", 24))

    draw_next_queue()

def draw_game_over(event=None):
    global gameover
    if gameover:    
        canvas.delete("all")
        #draw_grid()
        #draw_game_UI()
        #for row in range(rows):
        #    for col in range(cols):
        #        color = board[row][col]
        #        if color:
        #            x = start_x + col * block_size
        #            y = start_y + row * block_size
        #            draw_block(x, y, color)
        canvas.create_rectangle(138, 241, 438, 391, outline="white", width=3, fill="gray20", tags="gameover")
        canvas.create_text(288, 286, text="Game Over", fill="white", font=("Courier", 32), tags="gameover")
        canvas.create_text(288, 326, text=f"Score: {score}", fill="white", font=("Courier", 16), tags="gameover")
        retry_button = tk.Button(root, text="Retry", cursor="hand2", font=("Courier", 16), bg="#444444", fg="white", relief="raised", command=reset_game)
        canvas.create_window(288, 356, window=retry_button, tags="gameover")
    else:
        canvas.delete("gameover")


#SETTING BLOCK TICK MOVEMENT

def update_block():
    global current_piece, board, score, tick_speed, level, gameover
    if paused or gameover:
        root.after(get_tick_speed(level),update_block)
        return
    
    if not paused and not gameover:
        new_blocks = []
        for block in current_piece.blocks:
            x,y = block
            new_blocks.append([x,y])
        tick_speed = int(get_tick_speed(level))
        if current_piece.can_move_down(new_blocks)== True:
            current_piece.blocks = new_blocks
            current_piece.location[1] += 1
            update_screen()
            root.after(tick_speed, update_block)
            current_piece.lock_time = 0
        
        elif current_piece.can_move_down(new_blocks) == False :
            if current_piece.lock_time == 0:
                current_piece.lock_time = time.time()
            elif float(time.time()) - float(current_piece.lock_time) >= tick_speed/1000:
                current_piece.landed = True
                if current_piece.game_over_check():  # Check if the game is over
                    gameover = True
                    draw_game_over()
                    return  # Exit without spawning a new piece
                current_piece.fix_piece()
                clear_lines()
                score+=points_added
                spawn_new_piece()
            update_screen()
            root.after(get_tick_speed(level), update_block)



def draw_next_queue():
    x_offset = 450 + block_size
    y_offset = 150

    for i, piece_id in enumerate(next_queue):
        blocks = pieceidtoblocks(piece_id)
        color = piece_color(piece_id)
        for dx,dy in blocks:
            x = x_offset + dx*block_size
            y = y_offset + dy*block_size + i * 4 *block_size
            draw_block(x, y, color)



#def spawn_new_piece():
#    global current_piece, next_queue
#    piece_id = next_queue.pop(0)
#    current_piece = piece(pieceid = piece_id)
#    next_queue.append(random.randint(1,7))
#    update_screen()

def spawn_new_piece():
    global current_piece, next_queue, running, tick_speed
    

    # If no game over, proceed to spawn a new piece
    piece_id = next_queue.pop(0)
    current_piece = piece(pieceid=piece_id)
    next_queue.append(random.randint(1, 7))
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
    global board, level, total_lines_cleared, points_added, score, tick_speed
    new_board = []
    lines_cleared = 0
    points_added = 0

    for row in board:
        if all(cell is not None for cell in row):
            lines_cleared += 1  # Full row, will be cleared
        else:
            new_board.append(row)

    # Add empty rows at the top for each cleared line
    for _ in range(lines_cleared):
        new_board.insert(0, [None for _ in range(cols)])

    board = new_board

    # Update totals and scoring
    total_lines_cleared += lines_cleared
    level = 1 + total_lines_cleared // 10

    if lines_cleared == 1:
        points_added = 40 * level
    elif lines_cleared == 2:
        points_added = 100 * level
    elif lines_cleared == 3:
        points_added = 300 * level
    elif lines_cleared == 4:
        points_added = 1200 * level
    
    tick_speed = get_tick_speed(level)

    return points_added

def update_screen():
    global paused, gameover
    if not paused and not gameover:
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
    global paused,tick_speed
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
            canvas.create_text(288, 450 + i*20, text=line, fill="lightgray", font=("Courier",12),tags="Pause")

    else:
        canvas.delete("pause")
        update_screen()


#SETTING UP MOVEMENT FUNCTION
def rotate_piece_CCW(event=None):
    global paused, gameover
    if not paused or not gameover and current_piece:
        current_piece.ccw()
        current_piece.lock_time = 0
        update_screen()
def rotate_piece_CW(event=None):
    global paused, gameover
    if not paused or not gameover and current_piece:
        current_piece.cw()
        current_piece.lock_time = 0
        update_screen()
def moveblock_L(self):
    global paused,gameover
    if not paused or not gameover and current_piece:
        current_piece.l()
        current_piece.lock_time = 0
        update_screen()
def moveblock_R(self):
    global paused,gameover
    if not paused or not gameover and current_piece:
        current_piece.r()
        current_piece.lock_time = 0
        update_screen()
def softdrop(self):
    global paused,gameover
    if not paused or not gameover and current_piece:
        current_piece.soft()
        current_piece.lock_time = 0
        update_screen()
def harddrop(self):
    global paused,gameover
    if not paused or not gameover and current_piece:
        current_piece.hard()
        current_piece.lock_time = 0
        update_screen()

# Function to reset the game state  
def reset_game():
    global board, score, total_lines_cleared, level, next_queue, current_piece, running, tick_speed,gameover
    gameover = False
    board = [[None for _ in range(11)] for _ in range(29)]
    score = 0
    total_lines_cleared = 0
    level = 1
    next_queue = [random.randint(1,7) for _ in range(3)]
    current_piece = None
    running = True
    canvas.delete("all")
    spawn_new_piece()





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tetris Game")
    root.geometry("576x632")

    canvas = tk.Canvas(root, width=576, height=632, bg="black")
    canvas.pack()

    board = [[None for _ in range(11)] for _ in range(29)]

    block_size = 16
    cols = 11
    rows = 26 
    start_x = 200
    start_y = 100
    tick_speed = 800
    speeds = [ 720, 630, 550, 470, 380, 300, 220, 130, 100,
        80,  70,  50,  30,  20,  17]
    def get_tick_speed(level):
        return int(speeds[min(level-1,len(speeds)-1)])
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

    paused = False
    gameover = False
    score = 0
    total_lines_cleared = 0
    level = 1
    block = {"x":5, "y":0}


    #DEFINE BORDERS
    left_bound = -cols // 2
    right_bound = cols // 2
    bottom_bound = 84


    #NEXT QUEUE
    next_queue = [random.randint(1,7) for _ in range(3)]

    #STARTING GAME
    running = True

    start_button = tk.Button(root, text="▶ Start Game",cursor="hand2", font=("Courier", 16), bg="#444444",fg="white",relief="raised",command=start_game)
    canvas.create_window(288,150, window=start_button)
    root.bind("<Escape>", toggle_pause)
    root.bind("<z>",rotate_piece_CCW)
    root.bind("<Up>",rotate_piece_CW)
    root.bind("<Left>",moveblock_L)
    root.bind("<Right>",moveblock_R)
    root.bind("<Down>",softdrop)
    root.bind("<space>",harddrop)

    root.mainloop()

def board_to_boolean(board):
    """
    Convert a Tetris board to a boolean grid.
    Args:
        board (list of lists): Original board (2D list) with colors or None.
    Returns:
        list of lists: Boolean grid (True = occupied, False = empty).
    """
    return [[cell is not None for cell in row] for row in board]

def setup_tetris():
    # Create Tkinter root and UI elements
    root = tk.Tk()
    root.title("Tetris Game")
    root.geometry("576x632")

    canvas = tk.Canvas(root, width=576, height=632, bg="black")
    canvas.pack()

    board = [[None for _ in range(11)] for _ in range(29)]

    block_size = 16
    cols = 11
    rows = 26 
    start_x = 200
    start_y = 100
    tick_speed = 800
    speeds = [720, 630, 550, 470, 380, 300, 220, 130, 100, 80, 70, 50, 30, 20, 17]

    def get_tick_speed(level):
        return int(speeds[min(level-1, len(speeds)-1)])

    # Return everything you need
    return root, canvas, board, get_tick_speed
