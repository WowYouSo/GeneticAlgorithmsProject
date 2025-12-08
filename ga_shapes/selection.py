import random
from config import TOURNAMENT_SIZE

def tournament_selection(population, fitnesses):
    """
    Select one individual from population using tournament of k=TOURNAMENT_SIZE.
    Returns the selected individual (Chromosome).
    """
    candidates = random.sample(list(zip(population, fitnesses)), TOURNAMENT_SIZE)
    selected = max(candidates, key=lambda x: x[1])
    return selected[0]

def select_parents(population, fitnesses):
    """
    Select two parents using tournament selection independently.
    """
    return (
        tournament_selection(population, fitnesses),
        tournament_selection(population, fitnesses),
    )
