import math
from time import process_time

import pygame

from heightandcolourmap import HeightAndColourMap
from isocraftconstants import IsoCraftConstants


class IsoCraft:

    def __init__(self, width, height):

        self.height_map = HeightAndColourMap()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Iso Craft')
        self.background = (2, 2, 2)

        self.dy = IsoCraftConstants.BLOCK_SIZE * math.sin(math.pi / 6)
        self.dx = IsoCraftConstants.BLOCK_SIZE * math.cos(math.pi / 6)

        self.x_zero = width / 2.0
        self.y_zero = height * 0.9

        self.x_current = 0
        self.y_current = 0

    def run(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT:
                #         self.x_current += 2
                #     if event.key == pygame.K_RIGHT:
                #         self.x_current -= 2
                #     if event.key == pygame.K_UP:
                #         self.y_current += 2
                #     if event.key == pygame.K_DOWN:
                #         self.y_current -= 2

            self.x_current += 2
            self.y_current += 2

            time1 = process_time()
            self._display()
            print(process_time() - time1)
            pygame.display.flip()

    def _display(self):
        # Naive rendering from back to front.
        self.screen.fill(self.background)

        for x in range(IsoCraftConstants.VOLUME_DEPTH + self.x_current - 1, self.x_current - 1, -1):
            x_iso = x - self.x_current
            for y in range(IsoCraftConstants.VOLUME_DEPTH + self.y_current - 1, self.y_current - 1, -1):
                height_and_colour = self.height_map.get_height_and_colour(x, y)
                y_iso = y - self.y_current
                self._draw_column_at_iso(
                    x_iso,
                    y_iso,
                    height_and_colour[0],
                    height_and_colour[1])

    def _draw_column_at_iso(self, x, y, height, colour):
        # Draws a column at the given iso-metric coordinate, height (in block units) and colour
        x_abs = self.x_zero - x * self.dx + y * self.dx
        y_abs = self.y_zero - (x + y) * self.dy
        h_abs = IsoCraftConstants.BLOCK_SIZE * height

        # Modify the colours to give an illusion of lighting
        colour_bottom_right = colour
        colour_bottom_left = ([int(0.7 * x) for x in colour])
        colour_top = ([int(0.4 * x) for x in colour])

        # Bottom left face
        pygame.draw.polygon(self.screen,
                            colour_bottom_left,
                            [(x_abs, y_abs),
                             (x_abs - self.dx, y_abs - self.dy),
                             (x_abs - self.dx, y_abs - self.dy - h_abs),
                             (x_abs, y_abs - h_abs)
                             ]
                            )

        # Bottom right face
        pygame.draw.polygon(self.screen,
                            colour_bottom_right,
                            [(x_abs, y_abs),
                             (x_abs + self.dx, y_abs - self.dy),
                             (x_abs + self.dx, y_abs - self.dy - h_abs),
                             (x_abs, y_abs - h_abs)
                             ])

        # Top face
        pygame.draw.polygon(self.screen,
                            colour_top,
                            [(x_abs, y_abs - h_abs),
                             (x_abs + self.dx, y_abs - h_abs - self.dy),
                             (x_abs, y_abs - h_abs - 2 * self.dy),
                             (x_abs - self.dx, y_abs - h_abs - self.dy)
                             ])


def main():
    scene = IsoCraft(1280, 960)
    scene.run()


if __name__ == '__main__':
    main()
