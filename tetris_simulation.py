import random
from tetrisml import pieceidtoblocks, piece_color, center_piece

class Piece:
    def __init__(self, pieceid=0, location=(5, 0)):
        self.pieceid = pieceid
        self.blocks = pieceidtoblocks(pieceid)
        self.pivot = center_piece(pieceid)
        self.location = list(location)

    def get_absolute_blocks(self):
        abs_blocks = []
        for dx, dy in self.blocks:
            x = self.location[0] + dx
            y = self.location[1] + dy
            abs_blocks.append((x, y))
        return abs_blocks

    def rotated_blocks(self):
        return [(-dy, dx) for dx, dy in self.blocks]

class TetrisSimulation:
    def __init__(self, cols=11, rows=26):
        self.cols = cols
        self.rows = rows
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.piece = None
        self.moves = []
        self.spawn_new_piece()

    def spawn_new_piece(self):
        pieceid = random.randint(1, 7)
        self.piece = Piece(pieceid)

    def valid_position(self, abs_blocks):
        for x, y in abs_blocks:
            if x < 0 or x >= self.cols or y >= self.rows:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def move(self, dx):
        self.piece.location[0] += dx
        if not self.valid_position(self.piece.get_absolute_blocks()):
            self.piece.location[0] -= dx

    def rotate(self):
        new_blocks = self.piece.rotated_blocks()
        abs_blocks = [(self.piece.location[0]+x, self.piece.location[1]+y) for x,y in new_blocks]
        if self.valid_position(abs_blocks):
            self.piece.blocks = new_blocks

    def drop_one(self):
        self.piece.location[1] += 1
        if not self.valid_position(self.piece.get_absolute_blocks()):
            self.piece.location[1] -= 1
            self.lock_piece()
            return False
        return True

    def hard_drop(self):
        while self.drop_one():
            pass

    def lock_piece(self):
        for x, y in self.piece.get_absolute_blocks():
            if y < 0:
                self.game_over = True
                return
            self.board[y][x] = True
        self.clear_lines()
        self.spawn_new_piece()

    def clear_lines(self):
        new_board = []
        lines = 0
        for row in self.board:
            if all(row):
                lines += 1
            else:
                new_board.append(row)
        for _ in range(lines):
            new_board.insert(0, [None]*self.cols)
        self.board = new_board
        self.lines_cleared += lines
        self.score += lines * 100

    def compute_fitness(self):
        return self.lines_cleared

    def step(self, action):
        """
        action: 'left', 'right', 'rotate', 'drop', 'nothing'
        """
        if action == 'left':
            self.move(-1)
        elif action == 'right':
            self.move(1)
        elif action == 'rotate':
            self.rotate()
        elif action == 'drop':
            self.hard_drop()
        # always drop by 1 row
        alive = self.drop_one()

        if action == "drop":
            # Record the pieceid at this moment
            self.moves.append({"move": action, "pieceid": self.piece.pieceid})
        else:
            self.moves.append({"move": action})

        return alive
