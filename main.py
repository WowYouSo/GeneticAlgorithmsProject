import os
import random
import numpy as np
from PIL import Image

from config import (
    POPULATION_SIZE,
    NUM_GENERATIONS,
    MUTATION_RATE,
    SAVE_BEST_IMAGES,
    SAVE_EVERY_N_GENERATIONS,
    OUTPUT_DIR,
    RANDOM_SEED,
    ELITISM
)
from ga_shapes.chromosome import Chromosome
from ga_shapes.fitness import evaluate
from ga_shapes.selection import select_parents


def setup_environment():
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)

    if SAVE_BEST_IMAGES:
        os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_initial_population():
    """Create initial population of chromosomes."""
    return [Chromosome() for _ in range(POPULATION_SIZE)]


def save_best_image(chromosome, generation):
    """Render chromosome and save its image to disk."""
    img_array = chromosome.render_numpy()  # (H, W, 3) uint8
    img = Image.fromarray(img_array, mode="RGB")
    filename = os.path.join(OUTPUT_DIR, f"gen_{generation:04d}.png")
    img.save(filename)


def evolve():
    """Main GA loop."""
    setup_environment()
    population = create_initial_population()

    for gen in range(NUM_GENERATIONS):
        # 1. Evaluate fitness for current population
        fitnesses = [evaluate(ind) for ind in population]

        # 2. Logging: best and average fitness
        best_idx = int(np.argmax(fitnesses))
        best_fitness = fitnesses[best_idx]
        avg_fitness = float(np.mean(fitnesses))
        print(f"Generation {gen:4d} | best: {best_fitness:.4f} | avg: {avg_fitness:.4f}")

        best_individual = population[best_idx]

        # 3. Optionally save best image
        if SAVE_BEST_IMAGES and (gen % SAVE_EVERY_N_GENERATIONS == 0 or gen == NUM_GENERATIONS - 1):
            save_best_image(best_individual, gen)

        # 4. Create next generation
        next_population = []

        # Elitism: carry over the best individual unchanged
        if ELITISM and len(population) > 0:
            next_population.append(best_individual.clone())

        # Fill the rest of the population via selection + crossover + mutation
        while len(next_population) < POPULATION_SIZE:
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = parent1.crossover(parent2)

            if random.random() < MUTATION_RATE:
                child1.mutate()
            if random.random() < MUTATION_RATE:
                child2.mutate()

            next_population.append(child1)
            if len(next_population) < POPULATION_SIZE:
                next_population.append(child2)

        population = next_population

    # Final evaluation and save best
    fitnesses = [evaluate(ind) for ind in population]
    best_idx = int(np.argmax(fitnesses))
    best_individual = population[best_idx]
    print(f"Final best fitness: {fitnesses[best_idx]:.4f}")

    if SAVE_BEST_IMAGES:
        save_best_image(best_individual, NUM_GENERATIONS)


if __name__ == "__main__":
    evolve()
