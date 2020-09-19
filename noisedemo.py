from noise import Noise
import pygame

class NoiseDemo:
    STEP = 0.02
    def __init__(self, width, height):

        self.noise = Noise(256)
        self.cache = dict()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Perlin Noise Demo')
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.background = (2, 2, 2)

    def run(self):
        running = True
        octaves = 1

        while running:
            print(f"Rendering {octaves} octaves")
            self._display(octaves)
            pygame.display.flip()

            print(f"Rendered {octaves} octaves - waiting")
            waiting = True
            pygame.event.clear()
            while waiting:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        waiting = False
                        octaves = min(10, octaves + 1)
                    if event.key == pygame.K_DOWN:
                        waiting = False
                        octaves = max(1, octaves - 1)


    def _display(self, octaves):
        self.screen.fill(self.background)

        self.screen.blit(
            self.font.render(
                f"Number of Octaves: {octaves} - Use KEYUP and KEYDOWN to change number.",
                False, (255, 255, 255)),
            (40, 40)
        )

        pygame.draw.line(self.screen, (255, 255, 255), (0, self.height / 2), (self.width, self.height / 2))
        prev_x = 0
        prev_y = self.height / 2
        for i in range(1280):
            current =  self.noise.get_with_octaves(i * NoiseDemo.STEP, 0, octaves)
            cur_x = i * 1280 / self.width
            cur_y = current * self.height * 0.4 + self.height / 2
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (prev_x, prev_y),
                (cur_x, cur_y))
            prev_x = cur_x
            prev_y = cur_y


        for x in range(200):
            for y in range(200):
                current = self.noise.get_with_octaves(x * NoiseDemo.STEP, y * NoiseDemo.STEP, octaves)
                current += 0.7
                current /= 1.4
                current = int(current * 255)
                pygame.draw.line(
                    self.screen,
                    (current, current, current),
                    (x + self.width * 0.75, y + self.height * 0.75),
                    (x + self.width * 0.75, y + self.height * 0.75)
                )

    def get_with_octaves(self, x, y, octaves):
        key = (x, y, octaves)
        if key not in self.cache:
            self.cache[key] = self.noise.get_with_octaves(x, y, octaves)
        return self.cache[key]

def main():
    scene = NoiseDemo(1280, 960)
    scene.run()


if __name__ == '__main__':
    main()
