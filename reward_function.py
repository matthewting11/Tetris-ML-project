weights = {
    'height': -0.5,
    'lines_cleared': 1.0,
    'holes': -1.0,
    'bumpiness': -0.5,
}   #FOR TESTING ONLY. REAL WEIGHTS SHOULD BE LOADED FROM A CONFIG FILE


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

def count_lines_cleared(board):
    """
    Count the number of lines cleared in the Tetris board.
    
    Args:
        board (list of list of int): The Tetris board represented as a 2D list.
        
    Returns:
        int: The number of lines cleared.
    """
    return 1  # Placeholder for actual implementation

def compute_aggregate_height(board):
    """
    Compute the aggregate height of the Tetris board.
    
    Args:
        board (list of list of int): The Tetris board represented as a 2D list.
        
    Returns:
        float: The aggregate height of the board.
    """
    return 1.0  # Placeholder for actual implementation

def count_holes(board):
    """
    Count the number of holes in the Tetris board.
    
    Args:
        board (list of list of int): The Tetris board represented as a 2D list.
        
    Returns:
        int: The number of holes in the board.
    """
    return 1  # Placeholder for actual implementation

def compute_bumpiness(board):
    """
    Compute the bumpiness of the Tetris board.
    
    Args:
        board (list of list of int): The Tetris board represented as a 2D list.
        
    Returns:
        float: The bumpiness of the board.
    """
    return 1.0  # Placeholder for actual implementation


"""
Board is a 2D list of objects
Every tile is set as a None object
Once piece is placed, it is set to a color object



"""