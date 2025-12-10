from PIL import Image
import numpy as np
import os
from config import IMAGE_SIZE, TARGET_IMAGE_NAME, PIXEL_MSE_WEIGHT, EDGE_MSE_WEIGHT

_target_rgb = None
_target_edges = None

def _rgb_to_gray(rgb: np.ndarray) -> np.ndarray:
    """
    rgb: (H, W, 3), float32 [0,255]
    возвращает (H, W), float32
    """
    # простое усреднение каналов достаточно
    return rgb.mean(axis=2)

def _compute_edge_map(gray: np.ndarray) -> np.ndarray:
    """
    Примитивный градиент: разности по x и y.
    Возвращает (H, W) float32.
    """
    # сдвиги с wrap-around (окей для нас на 128x128)
    dx = np.roll(gray, -1, axis=1) - gray
    dy = np.roll(gray, -1, axis=0) - gray
    edges = np.sqrt(dx * dx + dy * dy)
    return edges

def _load_target():
    global _target_rgb, _target_edges
    path = os.path.join("target_images", TARGET_IMAGE_NAME)
    image = Image.open(path).convert("RGB").resize(IMAGE_SIZE)
    _target_rgb = np.array(image).astype(np.float32)

    gray = _rgb_to_gray(_target_rgb)
    _target_edges = _compute_edge_map(gray)


def evaluate(chromosome):
    global _target_rgb, _target_edges
    if _target_rgb is None:
        _load_target()


    candidate = chromosome.render_numpy().astype(np.float32)
    # return -np.mean((candidate - _target_rgb) ** 2)
    diff_rgb = candidate - _target_rgb
    mse_rgb = np.mean(diff_rgb * diff_rgb)

    # MSE по edge map
    cand_gray = _rgb_to_gray(candidate)
    cand_edges = _compute_edge_map(cand_gray)
    diff_edge = cand_edges - _target_edges
    mse_edge = np.mean(diff_edge * diff_edge)

    total = PIXEL_MSE_WEIGHT * mse_rgb + EDGE_MSE_WEIGHT * mse_edge
    return -total
