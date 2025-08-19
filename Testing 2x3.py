import tkinter as tk
import random
import json

cols = 10
rows = 28  # updated from 20 to 28
INFO_PANEL_WIDTH = 80
TOTAL_GAME_WIDTH = 300
block_size = 16

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

class Piece:
    def __init__(self, pieceid=0):
        self.pieceid = pieceid
        self.color = piece_color(pieceid)
        self.blocks = piece_to_blocks(pieceid)
        self.location = [cols // 2, 0]
        self.landed = False
        self.pivot = center_piece(pieceid)


    def rotate(self):
        # Rotate the piece clockwise
        new_blocks = []
        for block in self.blocks:
            x, y = block
            new_x = -y + self.pivot[0] + self.pivot[1]
            new_y = x - self.pivot[0] + self.pivot[1]
            new_blocks.append([new_x, new_y])
            self.blocks = new_blocks
            return self.blocks

class TetrisGame:
    def __init__(self,canvas, x_offset, y_offset,json_data=None,moves=None):
        canvas_width = (cols * block_size + 100)
        canvas_height = (rows * block_size + 60)
        #self.canvas = tk.Canvas(canvas, width=canvas_width, height=canvas_height, bg="black")
        self.x_offset = x_offset + INFO_PANEL_WIDTH  # Shift grid right for info panel
        self.y_offset = y_offset
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.current_piece = None
        self.running = True
        self.score = 0
        self.lines = 0
        self.level = 1

        self.moves = moves or []
        self.move_index = 0
        self.piece_placed = True
        if json_data:
            pass
        if not self.moves:
            self.spawn_new_piece()

    def play_json_move(self, move):
        # 1. Spawn the piece (ignores random bag)
        self.current_piece = Piece(move["pieceid"])  

        # 2. Apply rotation
        for _ in range(move["rotation"] % 4):
            self.current_piece.rotate()

        # 3. Move horizontally to target x
        dx = move["x"] - self.current_piece.location[0]
        self.current_piece.location[0] += dx

        # 4. Hard drop until it lands
        while self.can_move_down():
            self.current_piece.location[1] += 1
        self.lock_piece()
    def place_piece_from_move(self, move):
        # Create piece of given pieceid
        self.current_piece = Piece(move["pieceid"])

        # Rotate piece N times
        for _ in range(move["rotation"]):
            self.current_piece.rotate()

        # Set piece horizontal location to move['x']
        self.current_piece.location[0] = move["x"]
        self.current_piece.location[1] = 0  # start at top row

        # Drop piece immediately to lowest possible y
        while self.can_move_down():
            self.current_piece.location[1] += 1

        # Step back one, because last move down was invalid
        self.current_piece.location[1] -= 1

        # Lock the piece into the board
        self.lock_piece()

    def can_move_down(self):
        if self.current_piece is None:
            return
        for dx, dy in self.current_piece.blocks:
            x = self.current_piece.location[0] + dx
            y = self.current_piece.location[1] + dy + 1
            if y >= rows or (0 <= x < cols and self.board[int(y)][int(x)] is not None):
                return False
        return True

    def lock_piece(self):
        for dx, dy in self.current_piece.blocks:
            x = self.current_piece.location[0] + dx
            y = self.current_piece.location[1] + dy
            if 0 <= x < cols and 0 <= y < rows:
                self.board[int(y)][int(x)] = self.current_piece.color
        self.clear_lines()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = rows - len(new_board)
        if cleared:
            self.lines += cleared
            self.score += (cleared ** 2) * 100
            self.level = self.lines // 10 + 1
            for _ in range(cleared):
                new_board.insert(0, [None for _ in range(cols)])
            self.board = new_board

    def update(self):
        if self.current_piece is None:
            return
        if self.can_move_down():
            self.current_piece.location[1] += 1
        else:
            self.lock_piece()
            self.spawn_new_piece()
    def spawn_new_piece(self):
        self.current_piece = Piece(random.randint(1, 7))

    def render(self):
        if self.current_piece is None:
            return
        self.draw_info()
        self.draw_grid()
        self.draw_board()
        self.draw_piece()

    def draw_grid(self):
        for r in range(rows):
            for c in range(cols):
                x = self.x_offset + c * block_size
                y = self.y_offset + r * block_size
                self.draw_block(x, y, "black")

    def draw_board(self):
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                color = self.board[r][c]
                if color:
                    x = c * block_size
                    y = r * block_size
                    self.canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")

    def draw_piece(self):
        for dx, dy in self.current_piece.blocks:
            x = self.x_offset + (self.current_piece.location[0] + dx) * block_size
            y = self.y_offset + (self.current_piece.location[1] + dy) * block_size
            self.draw_block(x, y, self.current_piece.color)

    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")
'''
    def draw_info(self):
        info_x = self.x_offset - INFO_PANEL_WIDTH + 5
        info_y = self.y_offset
        self.canvas.create_text(info_x, info_y + 10, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Score:\n{self.score}")
        self.canvas.create_text(info_x, info_y + 60, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Lines:\n{self.lines}")
        self.canvas.create_text(info_x, info_y + 110, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Level:\n{self.level}")
'''


NUM_ROWS = 2
NUM_COLS = 3
GAMES = []

def main():
    root = tk.Tk()
    root.withdraw()
    window = tk.Toplevel(root)
    window.title("Multi Tetris AI Arena")
    
    canvas_width = NUM_COLS * (cols * block_size + 100)
    canvas_height = NUM_ROWS * (rows * block_size + 60)
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
    game = TetrisGame(canvas, x_offset=0, y_offset=0)
    canvas.pack()

    # Load the JSON file for the top-left game
    try:
        with open("C:/Users\matth\OneDrive\Documents\GitHub\Tetris-ML-project\generation_0_sample_0_moves.json", "r") as f:
            moves = json.load(f)
    except Exception as e:
        print("Error loading JSON:", e)
        moves = None

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x_offset = col * (cols * block_size + 80)
            y_offset = row * (rows * block_size + 60)
            game_width = cols * block_size + INFO_PANEL_WIDTH
            game_height = rows * block_size
            game_canvas = tk.Canvas(root, width=game_width, height=game_height, bg="black")
            game_canvas.place(x=x_offset, y=y_offset)  # position canvas
            game = TetrisGame(root, x_offset=0, y_offset=0)
            if row == 0 and col == 0:
                game.moves = moves
            else:
                game.moves = None
            GAMES.append(game)
            print(f"Game {len(GAMES)} canvas:", game_canvas)
            info_x = x_offset - INFO_PANEL_WIDTH + 5
            info_y = y_offset
            score = 0
            lines = 0
            level = 1
            canvas.create_text(info_x, info_y + 10, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Score:\n{score}")
            canvas.create_text(info_x, info_y + 60, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Lines:\n{lines}")
            canvas.create_text(info_x, info_y + 110, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Level:\n{level}")

    def tick_all_games():
        canvas.delete("all")
        for game in GAMES:
            if game.moves:
                if game.moves:    
                    move = game.moves.pop(0)
                    game.play_json_move(move)
                else:
                    game.update()
            
            game.render()
        window.after(300, tick_all_games)

    tick_all_games()
    root.mainloop()

if __name__ == '__main__':
    main()
