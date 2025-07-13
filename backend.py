import random


''' Logic for backend operations goes here 
0 = empty
1 = square - "yellow"
2 = long bar - "cyan"
3 = S piece - "green"
4 = Z piece - "red" 
5 = T piece - "purple"
6 = L piece - "orange"
7 = J piece - "blue"

landed = 1
falling = 0

Single: 40 points , multiplied by the level.
Double: 100 points , multiplied by the level.
Triple: 300 points , multiplied by the level.
Tetris: 1,200 points , multiplied by the level

'''

'''
5 subupdates, 1 main update
4 frames per subupdate --> 4 tiles dropped per second

60fps --> 16.67ms per frame


'''




board = [[piece() for _ in range(11)] for _ in range(27)]

class tile:
    def __init__(self,color):
        self.color = color

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

def center_piece(pieceid):
    # Define the pivot for each piece.
    # (These are one acceptable set of pivot points for classic Tetris.)
    if pieceid == 1:   # O-tetromino
        pivot = (0.5, 0.5)
    elif pieceid == 2:  # I-tetromino
        pivot = (1.5, 0.5)
    elif pieceid in (3, 4, 5, 7):  # S, Z, T, J
        pivot = (1, 0)
    elif pieceid == 6:  # L (or mirror; note: some implementations may choose a different pivot)
        pivot = (0, 1)
    elif pieceid == 0:  
        pivot = (0, 0)
    else:
        raise ValueError("Unknown piece")
    
    # Return the pivot point as a tuple (x, y). 
    return pivot


def test_position(board, oldpieceloc, newpieceloc):



class piece:
    def __init__(self, position,pieceid=0, landed=0):
        self.position = position
        self.pieceid = pieceid
        self.landed = landed
        self.blocks = pieceidtoblocks(pieceid)
        self.location = [5,25]
        self.pivot = center_piece(pieceid)
    def ccw(self):
        # Rotate the piece counter-clockwise
        new_blocks = []
        for block in self.blocks:
            x, y = block
            new_x = -y + self.pivot[0] + self.pivot[1]
            new_y = x - self.pivot[0] + self.pivot[1]
            new_blocks.append([new_x, new_y])
        #self.blocks = new_blocks
        return new_blocks
    def cw(self):
        # Rotate the piece clockwise
        new_blocks = []
        for block in self.blocks:
            x, y = block
            new_x = y - self.pivot[0] + self.pivot[1]
            new_y = -x + self.pivot[0] + self.pivot[1]
            new_blocks.append([new_x, new_y])
        #self.blocks = new_blocks
        return new_blocks
    def moveblock(self, direction):
        # Move the piece right
        #Left = False, Right = True
        if direction:
            new_location = [self.location[0]+1, self.location[1]]
        else:
            new_location = [self.location[0]-1, self.location[1]]
        #self.blocks = new_blocks
        return new_location
    
    def get_current_coords(self):
        current_coords = []
        for block in self.blocks:
            x, y = block
            current_x = x + self.location[0]
            current_y = y + self.location[1]
            current_coords.append([current_x, current_y])
        return current_coords
    
    def get_new_coords(self, nl=self.location, nb=self.blocks):
        new_coords = []
        for block in nb:
            x, y = block
            new_x = x + nl[0]
            new_y = y + nl[1]
            new_coords.append([new_x, new_y])
        return new_coords

    

    


        




