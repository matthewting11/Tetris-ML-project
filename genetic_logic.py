import random
import json
import subprocess

from tetris_simulation import TetrisSimulation, Piece

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
population_size = 20
num_weights = 4
weight_range = (-1.0, 1.0)
num_generations = 10
move_limit = 500

class solution_model:
    def __init__(self, weights, generation, fitness=0):
        self.weights = weights
        self.generation = generation
        self.fitness = fitness

    def get_weights(self):
        return self.weights

    def get_generation(self):
        return self.generation

    def get_fitness(self):
        return self.fitness

    def play_game(self, move_limit):
        game = TetrisSimulation()
        moves_played = 0

        while not getattr(game, "game_over", False) and moves_played < move_limit:
            best_action = "nothing"
            best_score = -float('inf')

            for action in ["left", "right", "rotate", "drop", "nothing"]:
                # Copy simulation
                sim = TetrisSimulation()
                sim.board = [row.copy() for row in game.board]
                sim.piece = Piece(game.piece.pieceid)
                sim.piece.blocks = game.piece.blocks.copy()
                sim.piece.location = game.piece.location.copy()

                sim.step(action)

                boolean_board = [[cell is not None for cell in row] for row in sim.board]
                lines_cleared = sim.lines_cleared
                aggregate_height = compute_aggregate_height(boolean_board)
                holes = count_holes(boolean_board)
                bumpiness = compute_bumpiness(boolean_board)

                score = (
                    self.weights[0] * lines_cleared
                    - self.weights[1] * aggregate_height
                    - self.weights[2] * holes
                    - self.weights[3] * bumpiness
                )

                if score > best_score:
                    best_score = score
                    best_action = action

            alive = game.step(best_action)
            moves_played += 1
            if not alive:
                break

        return game.compute_fitness(), game.moves

def create_initial_population(population_size, num_weights, weight_range, generation=0):
    population = []
    for _ in range(population_size):
        weights = [random.uniform(*weight_range) for _ in range(num_weights)]
        model = solution_model(weights, generation)
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
population = create_initial_population(population_size, num_weights, weight_range)

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

    # Pick 4 random models to save
    sample_indices = random.sample(range(len(model_records)), 4)
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
        child_model = solution_model(mutated_child_weights, generation + 1)
        new_population.append(child_model)

    # Next generation
    population = new_population
