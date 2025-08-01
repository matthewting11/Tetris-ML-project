import tkinter as tk
import random

cols = 10
rows = 28  # updated from 20 to 28
INFO_PANEL_WIDTH = 80
TOTAL_GAME_WIDTH = 300
block_size = (TOTAL_GAME_WIDTH - INFO_PANEL_WIDTH) // cols  # 22

class Piece:
    def __init__(self, pieceid=0):
        self.pieceid = pieceid
        self.color = self.piece_color()
        self.blocks = self.piece_to_blocks()
        self.location = [cols // 2, 0]
        self.landed = False

    def piece_to_blocks(self):
        pieces = {
            1: [[0, 0], [1, 0], [0, 1], [1, 1]],
            2: [[-1, 0], [0, 0], [1, 0], [2, 0]],
            3: [[0, 0], [1, 0], [-1, 1], [0, 1]],
            4: [[-1, 0], [0, 1], [0, 0], [1, 1]],
            5: [[0, 1], [-1, 1], [1, 1], [0, 0]],
            6: [[1, 0], [-1, 1], [0, 1], [1, 1]],
            7: [[-1, 0], [0, 0], [1, 0], [1, 1]]
        }
        return pieces.get(self.pieceid, [[0, 0]])

    def piece_color(self):
        colors = {
            1: "yellow", 2: "cyan", 3: "red", 4: "lightgreen",
            5: "purple", 6: "orange", 7: "lightblue"
        }
        return colors.get(self.pieceid, "gray")

class TetrisGame:
    def __init__(self, canvas, x_offset, y_offset):
        self.canvas = canvas
        self.x_offset = x_offset + INFO_PANEL_WIDTH  # Shift grid right for info panel
        self.y_offset = y_offset
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.current_piece = None
        self.running = True
        self.score = 0
        self.lines = 0
        self.level = 1
        self.spawn_new_piece()

    def spawn_new_piece(self):
        self.current_piece = Piece(random.randint(1, 7))

    def can_move_down(self):
        for dx, dy in self.current_piece.blocks:
            x = self.current_piece.location[0] + dx
            y = self.current_piece.location[1] + dy + 1
            if y >= rows or (0 <= x < cols and self.board[y][x] is not None):
                return False
        return True

    def lock_piece(self):
        for dx, dy in self.current_piece.blocks:
            x = self.current_piece.location[0] + dx
            y = self.current_piece.location[1] + dy
            if 0 <= x < cols and 0 <= y < rows:
                self.board[y][x] = self.current_piece.color
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
        if self.can_move_down():
            self.current_piece.location[1] += 1
        else:
            self.lock_piece()
            self.spawn_new_piece()

    def render(self):
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
        for r in range(rows):
            for c in range(cols):
                color = self.board[r][c]
                if color:
                    x = self.x_offset + c * block_size
                    y = self.y_offset + r * block_size
                    self.draw_block(x, y, color)

    def draw_piece(self):
        for dx, dy in self.current_piece.blocks:
            x = self.x_offset + (self.current_piece.location[0] + dx) * block_size
            y = self.y_offset + (self.current_piece.location[1] + dy) * block_size
            self.draw_block(x, y, self.current_piece.color)

    def draw_block(self, x, y, color):
        self.canvas.create_rectangle(x, y, x + block_size, y + block_size, fill=color, outline="white")

    def draw_info(self):
        info_x = self.x_offset - INFO_PANEL_WIDTH + 5
        info_y = self.y_offset
        self.canvas.create_text(info_x, info_y + 10, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Score:\n{self.score}")
        self.canvas.create_text(info_x, info_y + 60, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Lines:\n{self.lines}")
        self.canvas.create_text(info_x, info_y + 110, anchor="nw", fill="white", font=("Courier", 10, "bold"), text=f"Level:\n{self.level}")

NUM_ROWS = 2
NUM_COLS = 3
GAMES = []

def main():
    root = tk.Tk()
    root.title("Multi Tetris AI Arena")
    canvas_width = NUM_COLS * TOTAL_GAME_WIDTH
    canvas_height = NUM_ROWS * (rows * block_size + 20)
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()

    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            x_offset = c * TOTAL_GAME_WIDTH
            y_offset = r * (rows * block_size + 20)
            game = TetrisGame(canvas, x_offset, y_offset)
            GAMES.append(game)

    def tick_all_games():
        canvas.delete("all")
        for game in GAMES:
            game.update()
            game.render()
        root.after(300, tick_all_games)

    tick_all_games()
    root.mainloop()

if __name__ == '__main__':
    main()
