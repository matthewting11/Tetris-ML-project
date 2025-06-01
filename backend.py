print("hello")



''' Logic for backend operations goes here 
0 = empty
1 = square
2 = long bar
3 = S piece
4 = Z piece
5 = T piece
6 = L piece
7 = J piece


landed = 1
falling = 0

'''

'''
5 subupdates, 1 main update
4 frames per subupdate --> 4 tiles dropped per second

60fps --> 16.67ms per frame


'''




board = [[tile() for _ in range(11)] for _ in range(27)]

class tile:
    def __init__(self,color, filled=False):
        self.color = color
        self.filled = filled

class piece:
    def __init__(self, position,pieceid=0, landed=0,blocks = [],axisofrevolution = [0,0] ):
        self.position = position
        self.pieceid = pieceid
        self.landed = landed
        self.blocks = pieceidtoblocks(position)
        self.axisofrevolution = axisofrevolution

    def pieceidtoblocks(self, position):
        if position == 0:
            return []
        elif position == 1:
            return [[0, 0], [1, 0], [0, 1], [1, 1]]
        elif position == 2:
            return [[0, 0], [1, 0], [2, 0], [3, 0]]
        elif position == 3:
            return [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif position == 4:
            return [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif position == 5:
            return [[0, 0], [1, 0], [2, 0], [1, 1]]
        elif position == 6:
            return [[0, 0], [0, 1], [1, 1], [2, 1]]
        elif position == 7:
            return [[0, 0], [1, 0], [2, 0], [2, 1]]
        else:
            return [] ' FALLBACK CASE, SHOULD NOT HAPPEN'





