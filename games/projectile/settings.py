#: Screen/Window parameters.
CAPTION = "Projectile v0.1"
BG_COLOR = (0x00, 0x00, 0x00)

FPS_SIZE = 25
FPS_COLOR = (0xFF, 0x00, 0x00)

#: Grid Parameters
GRID_COLOR = (0xFF, 0xFF, 0xFF)
GRID_WIDTH = 1
GRID_ALPHA = 50

#: Difference in time between ticks
TICK_TIME = 10.0  # ms

#: Max number of rendered frames that can be skipped. This is mostly
#  relevant on slower machines, in case the time it takes to update the
#  game state is greater than `TICK_STEP`.
MAX_FRAMESKIP = 10

#: The size of a pixel in meters.
PIXEL_SIZE = 50.0

#: A constant to multiply modular speed constants.
SPEED_CONSTANT = 1 / TICK_TIME / PIXEL_SIZE
