import curses
from curses import wrapper, curs_set
from typing import Tuple, List, Any


def display(w, sprite):
    y = int(sprite[1])
    x = int(sprite[0])
    if x in range(0, curses.COLS) and y in range(0, curses.LINES):
        w.addstr(y, x, sprite[2])
    else:
        w.addstr(0, 0, f"display error: x={x}, y={y}")


def erase(w, sprite):
    display(w, (sprite[0], sprite[1], " " * len(sprite[2])))


def main(w: Any):
    # init curses
    curs_set(False)  # do not blink
    w.nodelay(True)  # no blocking input
    w.clear()
    # init vars
    paddle_speed = 4
    paddle_pattern = "swannswannswann"
    paddle_y = curses.LINES - 2
    paddle_x = (curses.COLS - len(paddle_pattern)) // 2
    brick_width = 8
    brick_pattern: str = "[" + ("-" * (brick_width - 2)) + "]"
    brick_lines = curses.LINES // 4
    brick_cols = curses.COLS // brick_width
    brick_states = [[True for _ in range(brick_cols)] for _ in range(brick_lines)]
    new_ball_x = (curses.COLS - len(paddle_pattern)) // 2
    new_ball_y = curses.LINES // 2
    ball_pattern = "o"
    ball_speed_x = 1
    ball_speed_y = 1
    ball_speed_ratio = 10000
    # init displays
    display(w, (paddle_x, paddle_y, paddle_pattern))
    display(w, (new_ball_x, new_ball_y, ball_pattern))
    for y in range(0, brick_lines):
        for x in range(0, brick_cols):
            display(w, (x * brick_width, y, brick_pattern))
    w.refresh()
    gameover = False
    iter = 0
    bounce = False
    while gameover is False:
        ball_x = new_ball_x
        ball_y = new_ball_y
        key = w.getch()
        if key == curses.KEY_LEFT:
            erase(w, (paddle_x, paddle_y, paddle_pattern))
            paddle_x = max(paddle_x - paddle_speed, 0)
        if key == curses.KEY_RIGHT:
            erase(w, (paddle_x, paddle_y, paddle_pattern))
            paddle_x = min(paddle_x + paddle_speed, curses.COLS - len(paddle_pattern))
        if iter % ball_speed_ratio == 0 or bounce:
            new_ball_x = ball_x + ball_speed_x
            new_ball_y = ball_y + ball_speed_y
            bounce = False
            if new_ball_x <= 0:
                new_ball_x = 0
                ball_speed_x = -ball_speed_x
                bounce = True
            if new_ball_x >= curses.COLS - 1:
                new_ball_x = curses.COLS - 1
                ball_speed_x = -ball_speed_x
                bounce = True
            if new_ball_y <= 0:
                new_ball_y = 0
                ball_speed_y = -ball_speed_y
                bounce = True
            if new_ball_y == paddle_y:
                if new_ball_x in range(paddle_x, paddle_x + len(paddle_pattern)):
                    ball_speed_y = -ball_speed_y
                    bounce = True
                else:
                    display(w, (curses.COLS / 2, curses.LINES / 2, "GAME OVER"))
                    gameover = True
            elif new_ball_y in range(0, brick_lines):
                brick_x = new_ball_x // len(brick_pattern)
                brick_y = new_ball_y
                if brick_x in range(0, brick_cols) and brick_states[brick_y][brick_x]:
                    erase(w, (brick_x * len(brick_pattern), brick_y, brick_pattern))
                    brick_states[brick_y][brick_x] = False
                    ball_speed_y = -ball_speed_y
                    bounce = True
            erase(w, (ball_x, ball_y, ball_pattern))
            display(w, (new_ball_x, new_ball_y, ball_pattern))
        display(w, (paddle_x, paddle_y, paddle_pattern))
        w.refresh()
        # w.addstr(0, 0, f"{ball_x} {ball_y}  ")
        # w.addstr(1, 0, f"{ball_speed_x} {ball_speed_y}  ")
        # w.addstr(2, 0, f"{new_ball_x} {new_ball_y}  ")
        # w.addstr(3, 0, f"{brick_x} {brick_y}  ")
        # w.addstr(4, 0, str(brick_states[0]))
        # w.addstr(5, 0, str(brick_states[1]))
        iter += 1
    w.nodelay(False)
    w.getch()


if __name__ == "__main__":
    wrapper(main)
