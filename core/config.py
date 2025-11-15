# core/config.py

GRID_SIZE = 20
CELL_SIZE = 30
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE

BASE_FPS = 5
FPS_INCREMENT = 1
LEVEL_UP_SCORE = 5

BASE_SENSING_RANGE = 3
BASE_SMARTNESS = 1

FOOD_PULSE_SPEED = 6
FOOD_PULSE_AMPLITUDE = 6

FONT_NAME = 'Arial'

# MAS / experiment settings
BUTTERFLY_MODE = True        # enable butterfly perturbation experiment
BUTTERFLY_STEP = 30         # step when tiny perturbation happens (1-based)
EVENT_LOG_PATH = "events/log.csv"  # events log to record runs
