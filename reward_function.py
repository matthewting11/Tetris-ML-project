weights = {
    'height': -0.5,
    'lines_cleared': 1.0,
    'holes': -1.0,
    'bumpiness': -0.5,
}   #FOR TESTING ONLY. REAL WEIGHTS SHOULD BE LOADED FROM A CONFIG FILE

sample_board = [
    [True, True, False, False, True],
    [True, True, True, False, True],
    [False, True, True, True, True],
    [False, False, True, False, False],
    [False, False, False, False, False]
]

"""
- - - - - - -
X - - - - - -
X X - - - - -
X X - - - - X
X X X X - - X
X X X - - - X
X X X X X X X
"""

boolean_board = [
    [False, False, False, False, False, False, False],
    [True,  False, False, False, False, False, False],
    [True,  True,  False, False, False, False, False],
    [True,  True,  False, False, False, False, True],
    [True,  True,  True,  True,  False, False, True],
    [True,  True,  True,  False, False, False, True],
    [True,  True,  True,  True,  True,  True,  True],
]



def score_possibility(board, weights):
    """
    Calculate the score of a given board position based on the weights provided.
    
    Args:
        board (list of list of int): The Tetris board represented as a 2D list.
        weights (dict): A dictionary containing weights for different scoring factors.
        
    Returns:
        float: The calculated score for the board position.
    """
    lines_cleared = count_lines_cleared(board)
    height = compute_aggregate_height(board)
    holes = count_holes(board)
    bumpiness = compute_bumpiness(board)    

    score = (weights['height'] * height +
             weights['lines_cleared'] * lines_cleared +
             weights['holes'] * holes +
             weights['bumpiness'] * bumpiness)
    
    return score

def count_lines_cleared(boolean_board):
    """
    Count the number of completely filled rows.
    """
    return sum(all(cell for cell in row) for row in boolean_board)


def compute_aggregate_height(boolean_board):
    """
    Sum of heights of all columns.
    """
    num_rows = len(boolean_board)
    num_cols = len(boolean_board[0])

    aggregate_height = 0

    for col in range(num_cols):
        col_height = 0
        for row in range(num_rows):
            if boolean_board[row][col]:
                col_height = num_rows - row
                break
        aggregate_height += col_height

    return aggregate_height

def count_holes(boolean_board):
    """
    Count empty cells that have at least one block above them.
    """
    num_rows = len(boolean_board)
    num_cols = len(boolean_board[0])

    holes = 0

    for col in range(num_cols):
        block_found = False
        for row in range(num_rows):
            if boolean_board[row][col]:
                block_found = True
            elif block_found and not boolean_board[row][col]:
                holes += 1

    return holes


def compute_bumpiness(boolean_board):
    """
    Sum of height differences between adjacent columns.
    """
    num_rows = len(boolean_board)
    num_cols = len(boolean_board[0])

    heights = []

    for col in range(num_cols):
        col_height = 0
        for row in range(num_rows):
            if boolean_board[row][col]:
                col_height = num_rows - row
                break
        heights.append(col_height)

    bumpiness = sum(abs(heights[col] - heights[col + 1]) for col in range(num_cols - 1))
    return bumpiness



"""
Board is a 2D list of BOOLEANS
"""

print(count_lines_cleared(boolean_board))  # Should return 1
print(compute_aggregate_height(boolean_board))  # Should return 23
print(count_holes(boolean_board))  # Should return 1
print(compute_bumpiness(boolean_board))  # Should return 8