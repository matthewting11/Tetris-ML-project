import tkinter as tk
import random
import json
import time
import math

cols = 11
rows = 26 # updated from 20 to 28
INFO_PANEL_WIDTH = 80
TOTAL_GAME_WIDTH = 300
block_size = 16
x_offset = cols * (cols * block_size + 80)
y_offset = rows * (rows * block_size + 60)

def piece_to_blocks(pieceid):
        pieces = {
            1: [[0, 0], [1, 0], [0, 1], [1, 1]],
            2: [[-1, 0], [0, 0], [1, 0], [2, 0]],
            3: [[0, 0], [1, 0], [-1, 1], [0, 1]],
            4: [[-1, 0], [0, 1], [0, 0], [1, 1]],
            5: [[0, 1], [-1, 1], [1, 1], [0, 0]],
            6: [[1, 0], [-1, 1], [0, 1], [1, 1]],
            7: [[-1, 0], [0, 0], [1, 0], [1, 1]]
        }
        return pieces.get(pieceid, [[0, 0]])

def piece_color(pieceid):
        colors = {
            1: "yellow", 2: "cyan", 3: "red", 4: "lightgreen",
            5: "purple", 6: "orange", 7: "lightblue"
        }
        return colors.get(pieceid, "gray")
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
  

class TetrisGame:
    def __init__(self,game_frame,game_width,game_height,r,c,moves, x_offset, y_offset,json_data=None,pieceid=0):
        global gameover,move
        gameover=False
        
        canvas_width = (cols * block_size + 100)
        canvas_height = (rows * block_size + 60)
        game_canvas = tk.Canvas(game_frame, width=game_width, height=game_height, bg="black")
        self.canvas = game_canvas

        self.x_offset = x_offset + INFO_PANEL_WIDTH  # Shift grid right for info panel
        self.y_offset = y_offset
        self.blocks = piece_to_blocks(self)
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.running = True

        self.score = 0
        self.lines = 0
        self.level = 1
        self.landed = False
        self.lock_time = 0
        self.moves = moves or []
        self.move_index = 0
        self.piece_placed = False
        self.location = [5, 0]    
        '''
        self.color = piece_color(pieceid)
        self.blocks = piece_to_blocks(pieceid)
        '''

        self.spawn_new_piece()        
        self.landed = False
  


        

        game_canvas.pack()
            
        game_canvas.create_text((cols * block_size+ INFO_PANEL_WIDTH)//2, 20, text=f"Game {r*NUM_COLS + c + 1}", fill="white", font=("Courier", 12, "bold"))
    




    def can_move_down(self,new_blocks):
        global score, points_added
        for x,y in new_blocks:
            absx = int(x+self.location[0])
            absy = int(y+self.location[1])
            if absy>=25 or self.board[int(absy)+1][int(absx)] is not None:
                if self.game_over_check():  # Check if the game is over
                    self.write_final_score()
                    running = False
                    return  # Exit without spawning a new piece
                return False
        return True
    def can_move_left(self,new_blocks):
        for x,y in new_blocks:
            boundx = x + self.location[0]
            boundy = y + self.location[1]
            if boundx<=0 or self.board[int(boundy)][int(boundx-1)] is not None:
                return False
        return True
    def can_move_right(self,new_blocks):
        for x,y in new_blocks:
            boundx = x+self.location[0]
            boundy = y + self.location[1]
            if boundx>=10 or self.board[int(boundy)][int(boundx+1)] is not None:
                return False
        return True
    def game_over_check(self):
        if self.landed:
            for x,y in self.blocks:
                if y + self.location[1] <= 4:
                    return True
        return False
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
    def rotate(self):
            # Rotate the piece clockwise
            new_blocks = []
            for block in self.blocks:
                x, y = block
                new_x = -y + self.pivot[0] + self.pivot[1]
                new_y = x - self.pivot[0] + self.pivot[1]
                new_blocks.append([new_x, new_y])
                                
            return new_blocks
    def hard(self):
        global points_added, score, gameover,move,pieceid
        #harddrop block on lowest possible level:
        if self.game_over_check():  # Check if the game is over
            gameover = True
            self.write_final_score()
            return  # Exit without spawning a new piece
        if gameover==True:
            self.update_screen()
            return
        if self.moves and self.move_index < len(self.moves):
            move = self.moves[self.move_index]
            pieceid = (move["pieceid"])
        if gameover is None:
            return
        for x,y in self.blocks:
            new_blocks = []
        for block in self.blocks:
            x,y = block
            new_y = y
            new_blocks.append([x,new_y])
        while self.can_move_down(new_blocks):
            self.blocks = new_blocks
            self.location[1]+=1
        self.landed = True
        self.fix_piece()
        self.clear_lines()
        self.score += points_added
        
        if self.game_over_check():  # Check if the game is over
            gameover = True
            self.write_final_score()
            return  # Exit without spawning a new piece
        self.update_screen()
        self.spawn_new_piece()
        
    '''
    def fix_piece(self):
        self.offset_x, self.offset_y = self.location  # piece's position on the grid
        for dx, dy in self.blocks:
            col = int(dx + self.offset_x)
            row = int(dy + self.offset_y)
            if 0 <= row < rows and 0 <= col < cols:
                self.board[row][col] = self.color
            self.update_screen()
          '''


    def fix_piece(self):
        offset_x, offset_y = self.location  # piece's position on the grid
        for dx, dy in self.blocks:
            col = int(dx + offset_x)
            row = int(dy + offset_y)
            current_color = []
            if 0 <= row < rows and 0 <= col < cols:
                current_color.append(color)
                
                self.board[row][col] = current_color[0]
                current_color.pop()
        self.update_screen()
        self.landed=True
        #print(self.board)


    def clear_lines(self):
        global board, level, points_added, tick_speed
        new_board = []
        lines_cleared = 0
        points_added = 0

        for row in self.board:
            if all(cell is not None for cell in row):
                lines_cleared += 1  # Full row, will be cleared
                print("line cleared!")
            else:
                new_board.append(row)

        # Add empty rows at the top for each cleared line
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(cols)])

        self.board = new_board

        # Update totals and scoring
        self.lines += lines_cleared
        self.level = 1 + lines_cleared // 10

        if lines_cleared == 1:
            points_added = 40 * self.level
        elif lines_cleared == 2:
            points_added = 100 * self.level
        elif lines_cleared == 3:
            points_added = 300 * self.level
        elif lines_cleared == 4:
            points_added = 1200 * self.level
        
        tick_speed = self.get_tick_speed()

        return points_added
    
    def get_tick_speed(self):
            speeds = [ 720, 630, 550, 470, 380, 300, 220, 130, 100, 80,  70,  50,  30,  20,  17]
            return int(speeds[min(self.level-1,len(speeds)-1)])
    
    def update_block(self):
        global move,pieceid, tick_speed, lock_time
        if gameover==True:
            return
        new_blocks = []
    
        for block in self.blocks:
            x,y = block
            new_x = x
            new_blocks.append([new_x,y])
        if move["x"]>5:
            for _ in range(move["rotation"]):
                self.rotate()
            
            while self.can_move_right(new_blocks)==True:   # set x position
                self.r()
                if self.location[0] == move["x"] or self.can_move_right(new_blocks)==False:
                    self.hard()
                    break
            
            for block in self.blocks:
                x,y = block
                new_blocks.append([x,y])
            tick_speed = int(self.get_tick_speed())
            self.blocks = new_blocks
            self.hard()
            self.update_screen()
            self.lock_time = 0
            #self.spawn_new_piece()
            self.update_block()
        elif move["x"]<5:
            for _ in range(move["rotation"]):
                self.rotate()
            
            while self.can_move_left(new_blocks)==True:   # set x position
                
                self.l()
                if self.location[0] == move["x"] or self.can_move_left(new_blocks)==False:
                    self.hard()
                    break

            for block in self.blocks:
                x,y = block
                new_blocks.append([x,y])
            tick_speed = int(self.get_tick_speed())
            self.blocks = new_blocks
            self.hard()
            self.update_screen()
            self.lock_time = 0
            #self.spawn_new_piece()
            self.update_block()

        elif move["x"]==5:
            for _ in range(move["rotation"]):
                self.rotate()
            
            self.hard()
            self.update_screen()
            #self.spawn_new_piece()
            self.update_block()


        '''
        elif self.can_move_down(new_blocks) == False :
            tick_speed = int(self.get_tick_speed())

            if self.lock_time == 0:
                self.lock_time = time.time()
            elif float(time.time()) - float(self.lock_time) >= tick_speed/1000:
                self.landed = True
                if self.game_over_check():  # Check if the game is over
                    gameover = True
                    self.write_final_score()
                    return  # Exit without spawning a new piece
                self.fix_piece()
                self.clear_lines()
                self.score+=points_added
                #self.spawn_new_piece()
            self.update_screen()
            self.canvas.after(tick_speed, self.update_block)
        '''
    
   
    def spawn_new_piece(self):
        global move,pieceid,color,gameover
        if gameover==True:
            return
        self.draw_grid()
        self.draw_info()

        if self.moves and self.move_index < len(self.moves):
            move = self.moves[self.move_index]
            pieceid = (move["pieceid"])
            #print("change")
        self.landed = False
        self.pivot = center_piece(pieceid)
        #print( self.move_index,pieceid, move["rotation"],move["x"])
        
        self.blocks = piece_to_blocks(pieceid)
        color = piece_color(pieceid)
        
        self.location=[5,0]
        #print(self.move_index,color,move["x"],move["rotation"])
        self.move_index +=1
        self.update_screen()
        if self.game_over_check():
            gameover==True
            self.write_final_score()
        self.update_block()
        

    def write_final_score(self):
    
        if gameover==True:  # Only write if the game is over
            info_x = 5  # position of info panel (adjust if needed)
            info_y = 150  # below the score/lines/level text
            #self.update_screen()
            self.canvas.create_text(
                info_x,
                info_y,
                anchor="nw",
                fill="red",
                font=("Courier", 12, "bold"),
                text=f"Game Over!\nFinal Score: {self.score}"
        
            )
        return
    
  
    def update_screen(self):
        global gameover
        if not gameover:
            self.canvas.delete("all")
            self.draw_grid()
            self.draw_info()
            for row in range(rows):
                for col in range(cols):
                    color = self.board[row][col]
                    if color:
                        x = self.x_offset + col * block_size
                        y = self.y_offset + row * block_size
                        self.draw_block(x,y,color)
            if True:
                #print("index",self.move_index)
                #print("id",pieceid)
                self.draw_piece()
                


    def draw_piece(self):
        for dx, dy in self.blocks:
            x = self.x_offset + (self.location[0] + dx) * block_size
            y = self.y_offset + (self.location[1] + dy) * block_size
            self.draw_block(x, y, color)

    def draw_info(self):
            info_x = self.x_offset - INFO_PANEL_WIDTH + 5
            info_y = self.y_offset

            self.canvas.create_text(info_x, info_y + 10, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Score:\n{self.score}")
            self.canvas.create_text(info_x, info_y + 60, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Lines:\n{self.lines}")
            self.canvas.create_text(info_x, info_y + 110, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Level:\n{self.level}")
    '''
    def draw_board(self):
        self.canvas.delete("all")
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        x*block_size, y*block_size,
                        (x+1)*block_size, (y+1)*block_size,
                        fill="cyan", outline="gray"
                    )
    '''
    def draw_grid(self):
                for r in range(rows):
                    for c in range(cols):
                        x = self.x_offset + c * block_size
                        y = self.y_offset + r * block_size
                        self.draw_block(x, y, "black")

    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")


NUM_ROWS = 2
NUM_COLS = 3
GAMES = []

def main():
    
    # Load the JSON file for the top-left game
    list_of_games = [
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_0_sample_0_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_0_sample_1_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_0_sample_2_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_0_sample_3_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_1_sample_0_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_1_sample_1_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_1_sample_2_moves.json",
        "C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_1_sample_3_moves.json"
    ]
    game_index = 0
    for batches_ran in range(math.ceil(len(list_of_games)/6)):
        root = tk.Tk()
        root.withdraw()
        window = tk.Toplevel(root)
        window.title("Multi Tetris AI Arena"+str(batches_ran+1))

        #BIG FRAME TO HOLD ALL GAMES
        games_frame = tk.Frame(window, bg="gray")    
        games_frame.pack(padx=20,pady=20)
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                #CANVAS FOR EACH GAME
                game_frame = tk.Frame(games_frame, bg="black")
                game_frame.grid(row=r, column=c, padx=10, pady=10)  # place in grid inside frame
                game_width = cols * block_size + INFO_PANEL_WIDTH
                game_height = rows * block_size
                
                
                if game_index<len(list_of_games):
                    with open(list_of_games[game_index], "r") as f:
                        moves = json.load(f)
                    game = TetrisGame(game_frame, game_width,game_height,r,c, x_offset=0, y_offset=0,moves=moves)

                else:
                    moves = None
                    game = TetrisGame(game_frame, game_width,game_height,r,c, x_offset=0, y_offset=0,moves=None)
                GAMES.append(game)
                game_index+=1
        is_whole = ((game_index/7) % 1) == 0
        if is_whole==True:
            window.after(2000)
            print("next")
            batches_ran+=1
                


    #window.geometry(f"{window_width}x{window_height}")
    #window.mainloop()


    def tick_all_games():
        for game in GAMES:
            game.update_screen()
            game.update_block()

            #root.after(800)

    tick_all_games()
    window.mainloop()
    

if __name__ == '__main__':
    main()
