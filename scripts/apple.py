import pyray as pr
from random import randint
from scripts.settings import TILE_SIZE, ROWS, COLS

class Apple:
    def __init__(self, snake) -> None:
        self.apple = pr.Rectangle(0, 0, TILE_SIZE, TILE_SIZE)
        self.spawn_apple([snake.head])

    def spawn_apple(self, restricted_rects) -> None:
        while True:
            self.apple.x = randint(0, ROWS - 1) * TILE_SIZE
            self.apple.y = randint(0, COLS - 1) * TILE_SIZE
            if not any(pr.check_collision_recs(self.apple, rect) for rect in restricted_rects):
                break

    def render(self) -> None:
        pr.draw_rectangle_rec(self.apple, pr.RED)