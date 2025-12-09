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
        # two focal points
        self.f1x = random.randint(0, WIDTH - 1)
        self.f1y = random.randint(0, HEIGHT - 1)
        self.f2x = random.randint(0, WIDTH - 1)
        self.f2y = random.randint(0, HEIGHT - 1)

        # sum of distances to focuses
        focal_distance = np.sqrt((self.f2x - self.f1x) ** 2 + (self.f2y - self.f1y) ** 2)
        self.sum_distances = random.uniform(focal_distance + 1, max(WIDTH, HEIGHT) * 2)

        self.color = np.array(
            [random.randint(0, 255) for _ in range(3)],
            dtype=np.float32,
        )
        self.alpha = random.uniform(0.0, 1.0)

    def mutate(self):
        self.f1x = int(np.clip(
            self.f1x + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, WIDTH - 1
        ))
        self.f1y = int(np.clip(
            self.f1y + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, HEIGHT - 1
        ))
        self.f2x = int(np.clip(
            self.f2x + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, WIDTH - 1
        ))
        self.f2y = int(np.clip(
            self.f2y + np.random.normal(0, GENE_MUTATION_SIGMA_POS),
            0, HEIGHT - 1
        ))
        focal_distance = np.sqrt((self.f2x - self.f1x) ** 2 + (self.f2y - self.f1y) ** 2)
        self.sum_distances = float(np.clip(
            self.sum_distances + np.random.normal(0, GENE_MUTATION_SIGMA_SIZE),
            focal_distance + 1,  # should be at least focal distance
            max(WIDTH, HEIGHT) * 2
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
        height, width, _ = canvas.shape

        # Bounding Box
        max_radius = int(self.sum_distances / 2) + 1

        center_x = (self.f1x + self.f2x) // 2
        center_y = (self.f1y + self.f2y) // 2

        y_min = max(0, center_y - max_radius)
        y_max = min(height, center_y + max_radius)
        x_min = max(0, center_x - max_radius)
        x_max = min(width, center_x + max_radius)

        if x_min >= x_max or y_min >= y_max:
            return

        # Coordinate grid
        y_grid, x_grid = np.ogrid[y_min:y_max, x_min:x_max]

        # distances to focus points
        d1 = np.sqrt((x_grid - self.f1x) ** 2 + (y_grid - self.f1y) ** 2)
        d2 = np.sqrt((x_grid - self.f2x) ** 2 + (y_grid - self.f2y) ** 2)

        # mask in/out of ellipsis
        mask_bool = (d1 + d2) <= self.sum_distances

        if not np.any(mask_bool):
            return

        mask = mask_bool.astype(np.float32)

        # color mixing
        canvas_roi = canvas[y_min:y_max, x_min:x_max]
        for c in range(3):
            canvas_roi[:, :, c] = (
                    (1.0 - self.alpha * mask) * canvas_roi[:, :, c]
                    + self.alpha * mask * self.color[c]
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
