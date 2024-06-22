import pyray as pr
from scripts.settings import WIN_SIZE, TITLE, FPS, TILE_SIZE
from scripts.snake import Snake
from scripts.apple import Apple

def main() -> None:
    pr.init_window(*WIN_SIZE, TITLE)
    pr.set_target_fps(FPS)

    snake = Snake()
    apple = Apple(snake)

    best_length = 0

    while not pr.window_should_close():
        snake.update(apple)
        if snake.dead:
            best_length = max(best_length, snake.length)
            snake = Snake()
            apple = Apple(snake)

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        apple.render()
        snake.render()
        pr.draw_text(f"length: {snake.length}, best: {best_length}", 0, 0, TILE_SIZE, pr.RAYWHITE)
        pr.end_drawing()
    pr.close_window()

if __name__ == "__main__":
    main()