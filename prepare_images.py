import os
from pathlib import Path

from PIL import Image

RAW_DIR = Path("raw_images")
TARGET_DIR = Path("target_images")

SIZES = [
    (64, 64),
    (128, 128),
]


def prepare():
    TARGET_DIR.mkdir(exist_ok=True)

    raw_files = [
        p for p in RAW_DIR.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]

    if not raw_files:
        raise RuntimeError(
            f"No images found in {RAW_DIR}. "
            f"Put some .jpg/.png files there first."
        )

    for img_path in raw_files:
        img = Image.open(img_path).convert("RGB")

        base_name = img_path.stem  # 'img1' from 'img1.jpg'

        for w, h in SIZES:
            resized = img.resize((w, h), Image.LANCZOS)
            out_name = f"{base_name}_{w}x{h}.png"
            out_path = TARGET_DIR / out_name
            resized.save(out_path)
            print(f"Saved {out_path}")


if __name__ == "__main__":
    prepare()
