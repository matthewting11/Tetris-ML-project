import random
import json
import subprocess

from tetris_simulation import TetrisSimulation, Piece

"""
Functions:
- count_lines_cleared(boolean_board)
    Counts the number of lines cleared in a theoretical Tetris board.

- compute_aggregate_height(boolean_board)
    Computes the aggregate height of blocks in a theoretical Tetris board.

- count_holes(boolean_board)
    Counts the number of holes in a theoretical Tetris board.

- compute_bumpiness(boolean_board)
- create_initial_population(population_size, num_weights, weight_range, generation=0)
- mutate(weights, mutation_rate=0.1, mutation_strength=0.2)
- crossover(weights1, weights2)
- solution_model class with methods:
    - get_weights()
    - get_generation()
    - get_fitness()
    - play_game(move_limit)


Data:
    Population: List of **solution_model** instances
        - weights: List of weights for the heuristic scoring functions
        - generation: Generation number
        - fitness: Fitness score based on game performance
        - moves: List of moves made during the game



WORKFLOW:
1. Define constants and how to define the stating generation.

2. for generation in range(num_generations):
    a. Create initial population of solution_model instances with random weights.
    
    b. For each model in the population:
        i. Play a game using the model's weights.
        ii. Compute fitness based on the game outcome.
    
    c. Sort models by fitness and save the best ones.
    
    d. Reproduce new models using crossover and mutation.
    
    e. Replace the old population with the new one.


"""



# Heuristic scoring functions
def count_lines_cleared(boolean_board):
    return sum(all(cell for cell in row) for row in boolean_board)

def compute_aggregate_height(boolean_board):
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

# GA parameters
population_size = 50
num_weights = 4
#weight_range = (-1.0, 1.0)
num_generations = 10
move_limit = 500
initialization_weight_ranges = {
    "lines_cleared": (0.1, 1.0),
    "aggregate_height": (-1.0, 0),
    "holes": (-1.0, 0),
    "bumpiness": (-1.0, 1.0)
}
scoring_functions = [
    count_lines_cleared,
    compute_aggregate_height,
    count_holes,
    compute_bumpiness
]


class solution_model:
    def __init__(self, weights, generation, scoring_funs, fitness=0):
        self.weights = weights
        self.generation = generation
        self.fitness = fitness
        self.scoring_funs = scoring_funs

    def get_weights(self):
        return self.weights

    def get_generation(self):
        return self.generation

    def get_fitness(self):
        return self.fitness

    def calc_move_score(self,board):
        score = 0
        for wnum in range(len(self.weights)):
            score += self.weights[wnum] * self.scoring_funs[wnum](board)
        return score



    def play_game(self, move_limit):
        game = TetrisSimulation(solution_model=self)
        moves_played = 0
    
            
        return game.compute_fitness(), game.moves


def create_initial_population(population_size, num_weights, generation=0):
    population = []
    for _ in range(population_size):
        for key, weight_range in initialization_weight_ranges.items():
            weights = [random.uniform(*weight_range) for _ in range(num_weights)]
        model = solution_model(weights, scoring_functions, generation)
        population.append(model)
    return population

def mutate(weights, mutation_rate=0.1, mutation_strength=0.2):
    new_weights = []
    for w in weights:
        if random.random() < mutation_rate:
            change = random.uniform(-mutation_strength, mutation_strength)
            new_weights.append(w + change)
        else:
            new_weights.append(w)
    return new_weights

def crossover(weights1, weights2):
    child_weights = []
    for w1, w2 in zip(weights1, weights2):
        chosen = random.choice([w1, w2])
        child_weights.append(chosen)
    return child_weights

# Initialize population
population = create_initial_population(population_size, num_weights)

processes = []


for generation in range(num_generations):
    print(f"\n=== Generation {generation} ===")
    model_records = []

    # Evaluate fitness
    for model in population:
        fitness, moves = model.play_game(move_limit)
        model.fitness = fitness
        model_records.append((model, moves))

    # Sort by fitness
    model_records.sort(key=lambda m: m[0].fitness, reverse=True)

    # Report best
    best_model, _ = model_records[0]
    print(f"Best fitness: {best_model.fitness}")

    # Pick 4 best models to save
    sample_indices = range(4)

    for i, idx in enumerate(sample_indices):
        model, moves = model_records[idx]
        filename = f"generation_{generation}_sample_{i}_moves.json"
        with open(filename, "w") as f:
            json.dump(moves, f)

    for p in processes:
        p.terminate()

    # Reset the list for this generation
    processes = []

    # Launch 4 replays
    for i in range(4):
        filename = f"generation_{generation}_sample_{i}_moves.json"
        p = subprocess.Popen(["python", "replay.py", filename])
        processes.append(p)


    # Reproduce
    num_parents = max(2, population_size // 5)
    parents = [m[0] for m in model_records[:num_parents]]
    new_population = []
    while len(new_population) < population_size:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child_weights = crossover(parent1.get_weights(), parent2.get_weights())
        mutated_child_weights = mutate(child_weights, mutation_rate=0.2, mutation_strength=0.3)
        child_model = solution_model(mutated_child_weights, scoring_functions, generation + 1)
        new_population.append(child_model)

    # Next generation
    population = new_population
