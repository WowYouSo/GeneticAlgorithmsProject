from PIL import Image
import numpy as np
import os
from config import IMAGE_SIZE, TARGET_IMAGE_NAME

_target_rgb = None

def _load_target():
    global _target_rgb
    path = os.path.join("target_images", TARGET_IMAGE_NAME)
    image = Image.open(path).convert("RGB").resize(IMAGE_SIZE)
    _target_rgb = np.array(image).astype(np.float32)

def evaluate(chromosome):
    global _target_rgb
    if _target_rgb is None:
        _load_target()
    candidate = chromosome.render_numpy().astype(np.float32)
    return -np.mean((candidate - _target_rgb) ** 2)
