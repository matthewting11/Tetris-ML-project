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
8 = T piece

landed = 1
falling = 0

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

class piece:
    def __init__(self, pieceid=0, landed=0,blocks = [],axisofrevolution = [0,0] ):
        self.pieceid = pieceid
        self.landed = landed
        self.blocks = blocks
        self.axisofrevolution = axisofrevolution

    def pieceidtoblocks(self):
        if self.pieceid == 0:
            return []
        elif self.pieceid == 1:
            return [[0, 0], [1, 0], [0, 1], [1, 1]]
        elif self.pieceid == 2:
            return [[0, 0], [1, 0], [2, 0], [3, 0]]
        elif self.pieceid == 3:
            return [[0, 0], [1, 0], [1, 1], [2, 1]]





