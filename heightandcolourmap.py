from isocraftconstants import IsoCraftConstants
from noise import Noise
from pageddatacache import PagedDataCache


class HeightAndColourMap:

    def __init__(self):
        self.noise = Noise()
        self.cache = PagedDataCache(
            self._get_height_and_colour_non_cached,
            IsoCraftConstants.VOLUME_DEPTH,
            IsoCraftConstants.VOLUME_DEPTH
        )

    def get_height_and_colour(self, x, y):
        # Cached version of below
        return self.cache.get(x, y)

    def _get_height_and_colour_non_cached(self, x, y):
        # Uses noise to determine the height of a given point.
        # Return a tuple of this height and the colour to render
        noise = HeightAndColourMap._normalise_noise(
            self.noise.get_with_octaves(
                x * IsoCraftConstants.NOISE_STEP, y * IsoCraftConstants.NOISE_STEP, IsoCraftConstants.OCTAVES
            )
        )
        colour = HeightAndColourMap._colour_from_normalised_noise(noise)

        # Scale
        height = int(noise * IsoCraftConstants.VOLUME_HEIGHT)
        return height, colour

    @staticmethod
    def _normalise_noise(n):
        # Noise will typically be in the range of -Sqrt(N/4) to + Sqrt(N/4) where N is the number of dimension
        # In our case we are using 2D noise - approximately -0.7 to 0.7
        # We  want to discount any noise <= Water_Level, then normalise the remaining portion.
        water_level = max(-0.7, IsoCraftConstants.WATER_LEVEL)
        return max(n - water_level, 0.0) / (0.7 - water_level)

    @staticmethod
    def _colour_from_normalised_noise(noise):
        return IsoCraftConstants.COLOUR_WATER if noise <= IsoCraftConstants.THRESHOLD_WATER \
            else IsoCraftConstants.COLOUR_BEACH if noise <= IsoCraftConstants.THRESHOLD_BEACH \
            else IsoCraftConstants.COLOUR_GRASS if noise <= IsoCraftConstants.THRESHOLD_GRASS \
            else IsoCraftConstants.COLOUR_ROCK if noise <= IsoCraftConstants.THRESHOLD_ROCK \
            else IsoCraftConstants.COLOUR_SNOW


