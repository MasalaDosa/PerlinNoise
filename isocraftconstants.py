
class IsoCraftConstants:
   
    # Height (in pixels) of a single block
    BLOCK_SIZE = 8

    # Length (in blocks) of the area to render.
    # If you half the BLOCK_SIZE the you should double the VOLUME_DEPTH
    VOLUME_DEPTH = 80

    # The maximum height (in blocks) - Used to scale vertically
    VOLUME_HEIGHT = 40

    # Noise lower than this is treated as water.
    WATER_LEVEL = -0.2

    # The smaller this number the smoother the landscape
    NOISE_STEP = 0.01

    # Number of octaves
    OCTAVES = 4

    # Colours for our various blocks
    COLOUR_WATER = (0, 45, 240)
    COLOUR_BEACH = (194, 178, 128)
    COLOUR_GRASS = (0, 240, 25)
    COLOUR_ROCK = (200, 160, 160)
    COLOUR_SNOW = (230, 230, 220)

    # And the thresholds which trigger blocks of this colour (from 0 to 1)
    THRESHOLD_WATER = 0
    THRESHOLD_BEACH = 0.05
    THRESHOLD_GRASS = 0.3
    THRESHOLD_ROCK = 0.5
    THRESHOLD_SHOW = 1.0
