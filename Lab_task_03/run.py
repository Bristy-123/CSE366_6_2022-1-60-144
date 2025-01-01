import pygame
import numpy as np
import random
from environment import Environment
from agent import Student

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class Scheduling Optimization")
font = pygame.font.Font(None, 24)

# Genetic Algorithm Parameters
population_size = 50
mutation_rate = 0.1
num_generations = 100
generation_delay = 1000  # Delay in milliseconds between generations

# Environment Setup
num_classes = 10
num_students = 5
num_time_slots = 6
environment = Environment(num_classes, num_students, num_time_slots)

# Genetic Algorithm Functions
def fitness(schedule):
    """
    Calculate the fitness of a schedule.
    - Minimize conflicts (classes assigned to unavailable students).
    - Maximize alignment with student preferences.
    """
    conflict_penalty = 0
    preference_penalty = 0

    for class_id, assigned_student in enumerate(schedule):
        student = environment.students[assigned_student]
        for time_slot in range(environment.num_time_slots):
            if student.availability[time_slot] == 0:  # Conflict
                conflict_penalty += 1
            elif time_slot not in student.preferences:  # Not preferred
                preference_penalty += 1 / student.preferences[time_slot]

    return conflict_penalty + preference_penalty


def selection(population):
    """Select the top half of the population based on fitness."""
    return sorted(population, key=fitness)[:population_size // 2]


def crossover(parent1, parent2):
    """Perform single-point crossover between two parents."""
    point = random.randint(1, len(parent1) - 1)
    return np.concatenate((parent1[:point], parent2[point:]))


def mutate(schedule):
    """Introduce random mutations to maintain genetic diversity."""
    for i in range(len(schedule)):
        if random.random() < mutation_rate:
            schedule[i] = random.randint(0, environment.num_students - 1)
    return schedule


# Initialize Population
population = environment.generate_population(population_size)

# Visualization Loop
running = True
best_solution = None
best_fitness = float('inf')
generation_count = 0
updates = []
max_updates = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm Step
    selected = selection(population)
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))
    population = next_generation

    # Evaluate the best solution
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    # Visualize Current Best Solution
    environment.draw_schedule(screen, font, best_solution)

    # Display Information
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness: {best_fitness:.2f}", True, (0, 0, 0))
    screen.blit(generation_text, (SCREEN_WIDTH - 200, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 200, 80))

    # Log Updates
    update_text = f"Gen {generation_count + 1}: Best Fitness = {best_fitness:.2f}"
    updates.append(update_text)
    if len(updates) > max_updates:
        updates.pop(0)  # Limit the number of displayed updates

    # Display Updates
    update_start_y = 650
    for i, update in enumerate(updates):
        update_surface = font.render(update, True, (0, 0, 0))
        screen.blit(update_surface, (50, update_start_y + i * 25))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1
    if generation_count >= num_generations:
        break

# Keep the window open after completion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
