IMAGE_SIZE = (128, 128)
NUM_GENES = 50
TARGET_IMAGE_NAME = "Hilma_af_Klint_Svanen_128x128.png"

POPULATION_SIZE = 200
NUM_GENERATIONS = 1000
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 20
ELITISM = True  # переносим лучшего в следующее поколение без изменений

# Visualization / saving
SAVE_BEST_IMAGES = True
SAVE_EVERY_N_GENERATIONS = 50
OUTPUT_DIR = "outputs"

# Reproducibility (optional)
RANDOM_SEED = 239

GENE_LOCAL_MUTATION_PROB = 0.8  # например 80% локальный сдвиг, 20% полный ресет

# Параметры локального шума (используются внутри генов)
GENE_MUTATION_SIGMA_POS = 5.0      # сдвиг координат (пиксели)
GENE_MUTATION_SIGMA_SIZE = 3.0     # сдвиг размеров
GENE_MUTATION_SIGMA_COLOR = 15.0   # сдвиг по цвету в каждом канале
GENE_MUTATION_SIGMA_ALPHA = 0.05   # сдвиг по альфе