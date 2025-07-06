import random

# Parameters
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
        self.time_survived = 0
        self.points_scored = 0
    
    def get_weights(self):
        return self.weights
    def get_generation(self):
        return self.generation
    def get_fitness(self):
        return self.fitness
    
    def play_game(self, move_limit):
        """
        Simulate a game with the current weights and return the fitness score.
        This is a placeholder for the actual game simulation logic.
        """
        return 1 #Placeholder for actual game logic to compute fitness score
    


def create_initial_population(population_size, num_weights, weight_range, generation=0):
    """
    Create a list of solution_model instances with random weights.
    
    Args:
        population_size (int): Number of agents to create.
        num_weights (int): How many weights each agent has.
        weight_range (tuple): (min, max) range for weights.
        generation (int): Starting generation number.

    Returns:
        list of solution_model
    """
    population = []
    for _ in range(population_size):
        weights = [random.uniform(*weight_range) for _ in range(num_weights)]
        model = solution_model(weights, generation)
        population.append(model)
    return population


population = create_initial_population(
    population_size=20,
    num_weights=4,               # e.g., lines, height, holes, bumpiness
    weight_range=(-1.0, 1.0),    # random weights between -1 and 1
)




def mutate(weights, mutation_rate=0.1, mutation_strength=0.2):
    """
    Mutate a list of weights.
    
    Args:
        weights (list of float): Original weights.
        mutation_rate (float): Probability to mutate each weight.
        mutation_strength (float): Max amount to add/subtract per mutation.
    
    Returns:
        list of float: Mutated weights.
    """
    new_weights = []
    for w in weights:
        if random.random() < mutation_rate:
            change = random.uniform(-mutation_strength, mutation_strength)
            new_weights.append(w + change)
        else:
            new_weights.append(w)
    return new_weights


def crossover(weights1, weights2):
    """
    Create a child by randomly combining weights from two parents.
    
    Args:
        weights1 (list of float): Parent 1 weights.
        weights2 (list of float): Parent 2 weights.
    
    Returns:
        list of float: Child weights.
    """
    child_weights = []
    for w1, w2 in zip(weights1, weights2):
        chosen = random.choice([w1, w2])
        child_weights.append(chosen)
    return child_weights




# Initialize the first generation
population = create_initial_population(population_size, num_weights, weight_range)

for generation in range(num_generations):
    print(f"\n=== Generation {generation} ===")
    
    # Evaluate fitness
    for model in population:
        fitness = model.play_game(move_limit)
        model.fitness = fitness

    # Sort by fitness descending
    population.sort(key=lambda m: m.fitness, reverse=True)

    # Report best fitness
    best = population[0]
    print(f"Best fitness: {best.fitness}")

    # Select top N parents (e.g., top 20%) -------------------------------------------ADJUST THIS PARAMETER
    num_parents = max(2, population_size // 5)
    parents = population[:num_parents]

    # Reproduce to create new population
    new_population = []

    while len(new_population) < population_size:
        # Randomly select 2 parents
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Crossover
        child_weights = crossover(parent1.get_weights(), parent2.get_weights())

        # Mutate
        mutated_child_weights = mutate(child_weights, mutation_rate=0.2, mutation_strength=0.3)

        # Create new solution_model
        child_model = solution_model(mutated_child_weights, generation + 1)

        new_population.append(child_model)

    # Replace old population
    population = new_population
