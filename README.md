# Genetic Algorithm for Image Approximation

## Project Overview

We have implemented 3 slightly different versions, which are located in the branches: `main`, `ellipsis-tilt`, and `alternative-selection`. The results of our experiments can be found in `experiments.docx`.

---

## Project Structure

### Core Files

#### `config.py`
Contains global parameters. Everything is fairly obvious. The main parameters include:
- Target image name
- Image pixel resolution

#### `main.py`
Contains the genetic algorithm itself. To run the program, simply execute:
```bash
python3 main.py
```

---

## `ga_shapes` Package

All other code is located in the `ga_shapes` directory:

### `chromosome.py`
Contains the chromosome class with `NUM_GENES` (from config) number of genes. Supports:
- **Crossover**
- **Mutation** (two types):
  - **More likely**: Local mutation of a random gene (slightly adjusting arguments)
  - **Less likely**: Complete chaotic change of a gene to something entirely different
- **Rendering** of the chromosome

### `fitness.py`
Basic fitness function using simple MSE (Mean Squared Error). No advanced techniques added.

### `gen.py`
Contains three gene types: **ellipses**, **line segments**, and **triangles**. Each gene supports:
- Random local mutation (`mutate` function)
- Drawing itself on the image (`apply` function)

#### Gene Descriptions

**Ellipse**
- Described by center coordinates, major and minor semi-axes
- No tilt support (tilt support available in the `ellipsis-tilt` branch)

**Triangle**
- Described by three point coordinates

**Line Segment**
- Described by two point coordinates and width

#### Gene Properties

Each gene has:
- **Color**: RGB color value
- **Alpha**: Transparency value (how much it lets the previous color through)

#### Rendering Formula

When drawing a gene, the color in each cell covered by the gene is processed using the formula:

```
new_color = (1 - alpha) * old_color + alpha * gen_color
```

*Feel free to experiment with this formula and modify it!*

### `selection.py`
Implements tournament selection. An alternative method is available where:
- Fitness is processed with softmax
- Selection is done with probability proportional to the result

---

## Directories

### `outputs/`
Contains visualized chromosomes saved every `SAVE_EVERY_N_GENERATIONS` generations.

### `raw_images/`
Contains original images downloaded from the internet.

### `target_images/`
Should contain your target images. The image name must match what you specified in `config.py`.

---

## Image Processing

### `prepare_images.py`
Takes images from `raw_images/` and converts them to 64 or 128 pixels resolution.

---

## Experimental Results

My experiments showed:

- **32×32 pixels**: Results are completely messy, nothing useful is produced
- **64×64 pixels**: Works moderately fast, but quality is still poor
- **128×128 pixels**: Works well ✓

---

## Getting Started

1. Place your target image in the `target_images/` directory
2. Update the target image name in `config.py`
3. Run the algorithm: `python3 main.py`
4. Check the `outputs/` directory for results

---

*Happy experimenting! 🧬🎨*
