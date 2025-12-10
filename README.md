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
