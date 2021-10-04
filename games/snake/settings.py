"""Global Settings."""

from pygame.color import Color

#: Screen/Window parameters.
CAPTION = "Snake v0.1"
BG_COLOR = Color(0x00, 0x00, 0x00)

#: FPS meter parameters.
DEBUG_SIZE = 25
DEBUG_COLOR = Color(0xFF, 0x00, 0x00)

#: Screen Size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 640
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

#: Grid parameters.
GRID_ALPHA = 50
GRID_COLOR = Color(0xFF, 0xFF, 0xFF)
GRID_LINE = 1
GRID_SIZE = (20, 20)  # Total number of cells in each coordinate.
GRID_STEP = 30  # The length of each cell in px.

#: UI parameters.
UI_HEIGHT = 40

#: Difference in time between ticks (Basically, the snake speed...)
TICK_STEP = 250.0  # ms
