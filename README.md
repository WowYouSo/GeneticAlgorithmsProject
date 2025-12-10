# Genetic Algorithm for Image Approximation

# Genetic Algorithm Image Reconstruction using Geometric Primitives

## Overview
This project implements a Genetic Algorithm that evolves a compositional picture made of simple geometric primitives (such as circles, lines, and triangles) to approximate a given target image. Each chromosome represents an entire image composed of 50 layered translucent genes-primitives. The GA mutates and recombines these primitives to reduce the pixel-wise difference to the target image.

## Problem Description
The core problem is to recreate a given 128×128 target image using a limited number of overlapping figures. The GA is used to search for an optimal combination of shape parameters that minimizes the difference to the target.

## Dataset
The dataset consists of a multiple 128×128 RGB target images. 

## Chromosome Encoding
Each chromosome represents a full candidate image as a fixed-length list of 50 genes. Each gene defines a single shape, and the sequence determines draw order. This encoding allows genetic operations such as crossover and mutation to operate on entire image descriptions.

## Gene Structure
Each gene represents one geometric primitive class inheritance from some basic primitive class with the following attributes:

- **Shape Type**: e.g., ellipse, line or triangle.
- **Arguments**: e.g., center coordinates, list of points, line parametrs etc.
- **Color (RGBA)**: red, green, blue values and alpha transparency.

When rendered in order, the 50 shapes form a complete image.

## Fitness Function
Each candidate is evaluated by comparing its rendered image to the target. The fitness function uses minus of mean squared error (MSE) between the candidate image and the target image. Higher fitness values indicate better approximation.

## Goals
- Reconstruct a recognizable 128×128 image using 50 translucent primitives.
- Apply genetic algorithms to a visual, creative problem.
- Explore the impact of encoding and representation in GA performance.
- Serve as a course project demonstrating GA usage beyond standard scheduling or routing problems.

## Implementation

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
Basic fitness function using simple MSE (Mean Squared Error). 

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

### `selection.py`
Implements tournament selection. An alternative method is available in branch alternative-selection where:
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

Can be found in experiments.docx

---

## Getting Started

1. Place your target image in the `target_images/` directory
2. Update the target image name in `config.py`
3. Run the algorithm: `python3 main.py`
4. Check the `outputs/` directory for results

---

