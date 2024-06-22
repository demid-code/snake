import pyray as pr
from raylib import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from scripts.settings import TILE_SIZE, ROWS, COLS, WIN_SIZE

class Snake:
    def __init__(self) -> None:
        self.head = pr.Rectangle(ROWS/2 * TILE_SIZE, COLS/2 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.body = []
        self.length = 3
        self.dir = pr.Vector2(0, 0)
        self.dead = False
        self.started = False
        self.key_wait = 0
        self.ticks = 0

    def set_dir(self, dir_x, dir_y) -> None:
        if self.key_wait < 1:
            self.key_wait = 3
            self.dir.x = dir_x
            self.dir.y = dir_y

    def update_dir(self) -> None:
        key_pressed = False
        if self.key_wait > 0:
            self.key_wait -= 1
        if pr.is_key_pressed(KEY_RIGHT) and self.dir.x != -1:
            self.set_dir(1, 0)
            key_pressed = True
        elif pr.is_key_pressed(KEY_LEFT) and self.dir.x != 1:
            self.set_dir(-1, 0)
            key_pressed = True
        elif pr.is_key_pressed(KEY_UP) and self.dir.y != 1:
            self.set_dir(0, -1)
            key_pressed = True
        elif pr.is_key_pressed(KEY_DOWN) and self.dir.y != -1:
            self.set_dir(0, 1)
            key_pressed = True
        
        if key_pressed and not self.started:
            self.started = True

    def update_body(self) -> None:
        self.body.append(pr.Rectangle(self.head.x, self.head.y, self.head.width, self.head.height))
        if len(self.body) >= self.length:
            del self.body[0]

    def check_is_dead(self) -> None:
        if (self.head.x < 0 or self.head.x + self.head.width > WIN_SIZE[0] or
            self.head.y < 0 or self.head.y + self.head.height > WIN_SIZE[1]):
            self.dead = True
            return

        if self.dir.x != 0 or self.dir.y != 0:
            if any(pr.check_collision_recs(body_rect, self.head) for body_rect in self.body):
                self.dead = True

    def update(self, apple) -> None:
        self.update_dir()
        if self.started:
            self.ticks = (self.ticks + 1) % 6
            self.check_is_dead()
            
            if self.ticks == 0:
                self.update_body()
                self.head.x += self.dir.x * TILE_SIZE
                self.head.y += self.dir.y * TILE_SIZE

                if pr.check_collision_recs(self.head, apple.apple):
                    self.length += 1
                    apple.spawn_apple(self.body + [self.head])

    def render(self) -> None:
        for rect in self.body:
            pr.draw_rectangle_rec(rect, pr.LIME)
        pr.draw_rectangle_rec(self.head, pr.GREEN)