import random
from abc import ABC, abstractmethod

import numpy as np
from config import SELECTION_STRATEGY
from config import TOURNAMENT_SIZE

class AbstractSelection(ABC):
    @abstractmethod
    def select(self,population, fitnesses):
        pass

class TournamentSelection(AbstractSelection):
    def select(self, population, fitnesses):
        """
        Select one individual from population using tournament of k=TOURNAMENT_SIZE.
        Returns the selected individual (Chromosome).
        """
        candidates = random.sample(list(zip(population, fitnesses)), TOURNAMENT_SIZE)
        selected = max(candidates, key=lambda x: x[1])
        return selected[0]

class SoftmaxSelection(AbstractSelection):

    def softmax(self,fitnesses):
        exps = np.exp(fitnesses)
        return exps / np.sum(exps)

    def select(self,population, fitnesses):
        """
        Select one individual from population with probability proportional to softmax of fitness function.
        Returns the selected individual (Chromosome).
        """
        probs = self.softmax(fitnesses)
        cdf = np.cumsum(probs)
        cdf[-1] = 1.0
        r = np.random.rand()
        idx = np.searchsorted(cdf, r, side="right")
        return population[idx]

SELECTIONS = {
    "tournament": TournamentSelection,
    "softmax": SoftmaxSelection
}
def select_parents(population, fitnesses):
    """
    Select two parents using tournament selection independently.
    """
    selection = SELECTIONS[SELECTION_STRATEGY]()
    return (
        selection.select(population, fitnesses),
        selection.select(population, fitnesses),
    )
