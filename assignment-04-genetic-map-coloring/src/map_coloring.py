# CSC 545/645 - Artificial Intelligence
# Assignment 4
# Riley Elliott
#
# Genetic Algorithm for the map-coloring problem

import random


# Fixed seed so the results can be repeated
random.seed(1)

# Four colors available for the map
colors = ["Red", "Blue", "Green", "Yellow"]


def read_state_file(file_name):
    # Read the states and their neighbors from the text file
    state_names = []
    neighbor_list = {}

    with open(file_name, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            state = parts[0]
            neighbors = parts[1:]

            state_names.append(state)
            neighbor_list[state] = neighbors

    # Give each state a number so it can be used in a list
    state_numbers = {}

    for i in range(len(state_names)):
        state_numbers[state_names[i]] = i

    # Make a list of borders between states
    borders = []

    for state in state_names:
        for neighbor in neighbor_list[state]:
            state1 = state_numbers[state]
            state2 = state_numbers[neighbor]

            # Do not add the same border twice
            if (state2, state1) not in borders:
                borders.append((state1, state2))

    return state_names, borders


def create_person(number_of_states):
    # One person represents one possible coloring of the map
    person = []

    for i in range(number_of_states):
        random_color = random.randint(0, 3)
        person.append(random_color)

    return person


def find_fitness(person, borders):
    # Higher fitness means more neighboring states
    # have different colors
    score = 0

    for state1, state2 in borders:
        if person[state1] != person[state2]:
            score += 1

    # In a normal CSP search, least-constraining value (LCV)
    # can choose a value that leaves more choices for neighbors.
    # This assignment uses a Genetic Algorithm instead, so here
    # fitness rewards map colorings with fewer conflicts.

    return score


def select_parent(population, borders):
    # Tournament selection:
    # randomly choose 3 people and keep the one with best fitness
    choices = random.sample(population, 3)

    best_person = choices[0]
    best_score = find_fitness(best_person, borders)

    for person in choices[1:]:
        current_score = find_fitness(person, borders)

        if current_score > best_score:
            best_person = person
            best_score = current_score

    return best_person


def crossover(parent1, parent2):
    # One-point crossover at a random location
    split_point = random.randint(1, len(parent1) - 1)

    child = parent1[:split_point] + parent2[split_point:]

    return child


def mutate(person, mutation_rate=0.02):
    # Each state has a small chance of changing color
    new_person = person.copy()

    for i in range(len(new_person)):
        if random.random() < mutation_rate:
            new_person[i] = random.randint(0, 3)

    return new_person


def genetic_algorithm(state_names, borders):
    # Main Genetic Algorithm
    population_size = 100
    max_generations = 5000
    number_of_states = len(state_names)

    population = []

    # Make the starting population
    for i in range(population_size):
        new_person = create_person(number_of_states)
        population.append(new_person)

    # A perfect score means every border is valid
    perfect_score = len(borders)

    # Go through the generations
    for generation in range(max_generations):
        best_person = population[0]
        best_score = find_fitness(best_person, borders)

        # Find the best person in this generation
        for person in population:
            current_score = find_fitness(person, borders)

            if current_score > best_score:
                best_person = person
                best_score = current_score

        # Stop if all border constraints are satisfied
        if best_score == perfect_score:
            return best_person, generation, best_score

        new_population = []

        # Keep the best solution from this generation
        new_population.append(best_person.copy())

        # Make the rest of the next generation
        while len(new_population) < population_size:
            parent1 = select_parent(population, borders)
            parent2 = select_parent(population, borders)

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    # If the generation limit is reached, return the best result found
    best_person = population[0]
    best_score = find_fitness(best_person, borders)

    for person in population:
        current_score = find_fitness(person, borders)

        if current_score > best_score:
            best_person = person
            best_score = current_score

    return best_person, max_generations, best_score


def count_violations(solution, borders):
    # Count neighboring states that incorrectly have the same color
    violations = 0

    for state1, state2 in borders:
        if solution[state1] == solution[state2]:
            violations += 1

    return violations


def show_solution(state_names, solution):
    # Print each state and its final color
    print("\nFinal Map Coloring")
    print("------------------")

    for i in range(len(state_names)):
        state = state_names[i]
        color = colors[solution[i]]

        print(state, "=", color)


def run_map(file_name, map_name):
    # Read and solve one map-coloring problem
    print("\n================================")
    print(map_name)
    print("================================")

    state_names, borders = read_state_file(file_name)

    solution, generations, fitness = genetic_algorithm(
        state_names, borders
    )

    show_solution(state_names, solution)

    violations = count_violations(solution, borders)

    print("\nResults")
    print("-------")
    print("Number of regions:", len(state_names))
    print("Number of border constraints:", len(borders))
    print("Number of generations:", generations)
    print("Number of constraint violations:", violations)
    print("Fitness score:", fitness, "out of", len(borders))


# Run the two problems required for Assignment 4
run_map("us_states_10_ij.txt", "10-State Map")
run_map("us_states_51_ij.txt", "51-Region Map")
