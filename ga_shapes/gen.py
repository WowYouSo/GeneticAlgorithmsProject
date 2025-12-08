import random
import numpy as np
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
from config import (
    IMAGE_SIZE,
    GENE_MUTATION_SIGMA_POS,
    GENE_MUTATION_SIGMA_SIZE,
    GENE_MUTATION_SIGMA_COLOR,
    GENE_MUTATION_SIGMA_ALPHA,
)

WIDTH, HEIGHT = IMAGE_SIZE

class AbstractGene(ABC):
    @abstractmethod
    def apply(self, canvas):
        pass

    @abstractmethod
    def mutate(self) -> None:
        pass

class EllipseGene(AbstractGene):
    def __init__(self):
        self.cx = random.randint(0, WIDTH - 1)
        self.cy = random.randint(0, HEIGHT - 1)
        self.rx = random.randint(1, WIDTH)
        self.ry = random.randint(1, HEIGHT)
        self.color = np.array(
            [random.randint(0, 255) for _ in range(3)],
            dtype=np.float32,
        )
        self.alpha = random.uniform(0.0, 1.0)

    def mutate(self):
        # Локовые сдвиги координат и размеров
        self.cx = int(np.clip(
            self.cx + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, WIDTH - 1
        ))
        self.cy = int(np.clip(
            self.cy + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, HEIGHT - 1
        ))
        self.rx = int(np.clip(
            self.rx + np.random.normal(0, GENE_MUTATION_SIGMA_SIZE),
            1, WIDTH
        ))
        self.ry = int(np.clip(
            self.ry + np.random.normal(0, GENE_MUTATION_SIGMA_SIZE),
            1, HEIGHT
        ))

        # Цвет
        self.color = np.clip(
            self.color + np.random.normal(0, GENE_MUTATION_SIGMA_COLOR, size=3),
            0, 255
        )

        # Альфа
        self.alpha = float(np.clip(
            self.alpha + np.random.normal(0, GENE_MUTATION_SIGMA_ALPHA),
            0.00, 0.99
        ))

    def apply(self, canvas: np.ndarray) -> None:
        mask = Image.new("L", IMAGE_SIZE, 0)
        draw = ImageDraw.Draw(mask)
        bbox = [self.cx - self.rx,
                self.cy - self.ry,
                self.cx + self.rx,
                self.cy + self.ry]
        draw.ellipse(bbox, fill=255)
        mask_np = np.array(mask, dtype=np.float32) / 255.0

        for c in range(3):
            canvas[:, :, c] = (
                (1.0 - self.alpha * mask_np) * canvas[:, :, c]
                + self.alpha * mask_np * self.color[c]
            )


class TriangleGene(AbstractGene):
    def __init__(self):
        self.points = [
            (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            for _ in range(3)
        ]
        self.color = np.array(
            [random.randint(0, 255) for _ in range(3)],
            dtype=np.float32,
        )
        self.alpha = random.uniform(0.0, 1.0)

    def mutate(self):
        new_points = []
        for (x, y) in self.points:
            nx = int(np.clip(
                x + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
                0, WIDTH - 1
            ))
            ny = int(np.clip(
                y + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
                0, HEIGHT - 1
            ))
            new_points.append((nx, ny))
        self.points = new_points

        self.color = np.clip(
            self.color + np.random.normal(0, GENE_MUTATION_SIGMA_COLOR, size=3),
            0, 255
        )

        self.alpha = float(np.clip(
            self.alpha + np.random.normal(0, GENE_MUTATION_SIGMA_ALPHA),
            0.00, 0.99
        ))

    def apply(self, canvas: np.ndarray) -> None:
        mask = Image.new("L", IMAGE_SIZE, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(self.points, fill=255)
        mask_np = np.array(mask, dtype=np.float32) / 255.0

        for c in range(3):
            canvas[:, :, c] = (
                (1.0 - self.alpha * mask_np) * canvas[:, :, c]
                + self.alpha * mask_np * self.color[c]
            )


class LineGene(AbstractGene):
    def __init__(self):
        self.x1 = random.randint(0, WIDTH - 1)
        self.y1 = random.randint(0, HEIGHT - 1)
        self.x2 = random.randint(0, WIDTH - 1)
        self.y2 = random.randint(0, HEIGHT - 1)
        self.width = random.randint(1, 5)
        self.color = np.array(
            [random.randint(0, 255) for _ in range(3)],
            dtype=np.float32,
        )
        self.alpha = random.uniform(0.0, 1.0)

    def mutate(self):
        self.x1 = int(np.clip(
            self.x1 + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, WIDTH - 1
        ))
        self.y1 = int(np.clip(
            self.y1 + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, HEIGHT - 1
        ))
        self.x2 = int(np.clip(
            self.x2 + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, WIDTH - 1
        ))
        self.y2 = int(np.clip(
            self.y2 + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, HEIGHT - 1
        ))

        self.width = int(np.clip(
            self.width + np.random.normal(0, 1.0),
            1, 10
        ))

        self.color = np.clip(
            self.color + np.random.normal(0, GENE_MUTATION_SIGMA_COLOR, size=3),
            0, 255
        )

        self.alpha = float(np.clip(
            self.alpha + np.random.normal(0, GENE_MUTATION_SIGMA_ALPHA),
            0.00, 0.99
        ))

    def apply(self, canvas: np.ndarray) -> None:
        mask = Image.new("L", IMAGE_SIZE, 0)
        draw = ImageDraw.Draw(mask)
        draw.line((self.x1, self.y1, self.x2, self.y2), fill=255, width=self.width)
        mask_np = np.array(mask, dtype=np.float32) / 255.0

        for c in range(3):
            canvas[:, :, c] = (
                (1.0 - self.alpha * mask_np) * canvas[:, :, c]
                + self.alpha * mask_np * self.color[c]
            )
