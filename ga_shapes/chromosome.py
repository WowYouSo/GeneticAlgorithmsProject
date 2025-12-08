import random
import numpy as np
from ga_shapes.gen import EllipseGene, TriangleGene, LineGene
from config import IMAGE_SIZE, NUM_GENES, GENE_LOCAL_MUTATION_PROB
import copy

GENE_CLASSES = [EllipseGene, TriangleGene, LineGene]


class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes if genes else [
            random.choice(GENE_CLASSES)() for _ in range(NUM_GENES)
        ]

    @classmethod
    def from_parents(cls, g1, g2, split_point):
        # Делаем НОВЫЕ гены через deepcopy, а не делим те же объекты
        parent_genes = g1.genes[:split_point] + g2.genes[split_point:]
        new_genes = [copy.deepcopy(g) for g in parent_genes]
        return cls(genes=new_genes)

    def clone(self):
        # Полная копия хромосомы со своими объектами генов
        return Chromosome(genes=[copy.deepcopy(g) for g in self.genes])

    def mutate(self):
        """Мутируем один случайный ген:
        - с вероятностью GENE_LOCAL_MUTATION_PROB: локовый сдвиг параметров гена
        - иначе: полностью пересоздаём ген случайного типа
        """
        index = random.randint(0, NUM_GENES - 1)
        if random.random() < GENE_LOCAL_MUTATION_PROB:
            # локовая мутация параметров того же гена
            self.genes[index].mutate()
        else:
            # жёсткий ресет гена (возможно другого типа)
            self.genes[index] = random.choice(GENE_CLASSES)()

    def crossover(self, other):
        split = random.randint(1, NUM_GENES - 2)
        return (
            Chromosome.from_parents(self, other, split),
            Chromosome.from_parents(other, self, split),
        )

    def render_numpy(self):
        canvas = np.ones((*IMAGE_SIZE, 3), dtype=np.float32) * 255.0
        for gene in self.genes:
            gene.apply(canvas)
        return np.clip(canvas, 0, 255).astype(np.uint8)
