import random
from tetrisml import pieceidtoblocks, piece_color, center_piece
from genetic_logic import solution_model


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

    def get_blocks_relative(self):
        rel_blocks = []
        for dx, dy in self.blocks:
            rel_blocks.append((dx, dy))
        return rel_blocks

    def rotated_blocks(self):
        return [(-dy, dx) for dx, dy in self.blocks]

    def check_valid_spawn(self, cols):
        abs_blocks = self.get_absolute_blocks()
        for x, y in abs_blocks:
            if x < 0 or x >= cols or y < 0:
                return False
        return True

    def get_piece_id(self):
        return self.pieceid

class TetrisSimulation:
    def __init__(self, sol_model, cols=11, rows=26):
        self.cols = cols
        self.rows = rows
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.piece = None
        self.moves = []
        self.sol_model = sol_model
        self.define_new_piece()

    def define_new_piece(self):
        pieceid = random.randint(1, 7)
        self.piece = Piece(pieceid)

    def valid_position(self, abs_blocks):
        for x, y in abs_blocks:
            if x < 0 or x >= self.cols or y >= self.rows:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def rotate(self):
        new_blocks = self.piece.rotated_blocks()
        abs_blocks = [(self.piece.location[0]+x, self.piece.location[1]+y) for x,y in new_blocks]
        if self.valid_position(abs_blocks):
            self.piece.blocks = new_blocks

    def make_a_move_bitch(self):
        possibilities_undropped = []
        possibilities_rot_shift = []

        #Get all possible rotations
        basecoords = []
        rotation_nums = []
        for _ in range(4):
            basecoords.append(self.piece.get_blocks_relative())
            rotation_nums.append(_)
            self.piece.rotated_blocks()
        

        #Get all possible horizontal shifts, MORON CODE

        for shift in range(-2, self.cols+2):
            for possible_rotation in range(len(basecoords)):
                new_piece = Piece(pieceid=self.piece.pieceid, location=(shift, 0))
                new_piece.blocks = basecoords[possible_rotation]
                if self.valid_position(new_piece.get_absolute_blocks()):
                    possibilities_undropped.append(new_piece.get_absolute_blocks())
                    possibilities_rot_shift.append((rotation_nums[possible_rotation],shift))
        
        #convert undropped to dropped, get output boards
        dropped_possible_boards = []
        maximum_score=  -10000
        best_board = None
        best_rot_shift = (0,0)

        for undropped in possibilities_undropped:
            sim_board = simulated_board(self.board, undropped)
            score = self.sol_model.calc_move_score(sim_board.place_drop_export())
            if score > maximum_score:
                best_board = sim_board.get_board()
                maximum_score = score
        
        return best_board, self.piece.get_piece_id(), best_rot_shift
        
        
        

        
        

        
        
class simulated_board:
    def __init__(self, board, new_piece_absolute_blocks=None):
        self.board = board
        self.new_piece_absolute_blocks = new_piece_absolute_blocks if new_piece_absolute_blocks else []
        #new_piece_absolute_blocks: [(0,5),(1,5),(2,5),(1,4)]

    def get_board(self):
        return self.board

    def check_if_should_be_placed(self):
        for x, y in self.new_piece_absolute_blocks:
            if any(self.board[x][y]) or any (y<0):
                return True
        return False
    
    def down_1(self):
        for tile in self.new_piece_absolute_blocks:
            tile[1] = tile[1]+1

    def up_1(self):
        for tile in self.new_piece_absolute_blocks:
            tile[1] = tile[1]-1

    def fix_piece(self):
        for x,y in self.new_piece_absolute_blocks:
            self.board[x][y] = True

    def place_drop_export(self):
        dist_dropped = 0
        while dist_dropped < len(self.simulated_board):
            if(self.check_if_should_be_placed):
                self.up_1
                self.fix_piece
                return simulated_board
            else:
                self.down_1
                dist_dropped +=1



"""
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
"""