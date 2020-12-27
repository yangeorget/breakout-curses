import curses
from curses import wrapper, curs_set


paddle_speed = 4
paddle_pattern = "_----------_"
brick_std_pattern = "[------]"
ball_pattern = "o"


def debug(w, ball_x, ball_y, ball_speed_x, ball_speed_y, brick_states):
    w.addstr(0, 0, f"{ball_x} {ball_y}")
    w.addstr(1, 0, f"{ball_speed_x} {ball_speed_y}  ")
    w.addstr(2, 0, str(brick_states[0]))
    w.addstr(3, 0, str(brick_states[1]))


def display(w, sprite):
    w.addstr(int(sprite[1]), int(sprite[0]), sprite[2])


def erase(w, sprite):
    display(w, (sprite[0], sprite[1], " " * len(sprite[2])))


def count_bricks(brick_states):
    count = 0
    for line in brick_states:
        count += sum(line)
    return count


def main(w):
    # init curses
    curs_set(False)  # do not blink
    w.nodelay(True)  # no blocking input
    w.clear()
    # init vars
    ball_speed_x = .0001
    ball_speed_y = .0001
    paddle_y = curses.LINES - 2
    paddle_x = (curses.COLS - len(paddle_pattern)) // 2
    brick_lines = curses.LINES // 4
    brick_cols = curses.COLS // len(brick_std_pattern)
    brick_states = [[True for _ in range(brick_cols)] for _ in range(brick_lines)]
    ball_x = (curses.COLS - len(paddle_pattern)) // 2
    ball_y = curses.LINES // 2
    # init displays
    display(w, (paddle_x, paddle_y, paddle_pattern))
    display(w, (ball_x, ball_y, ball_pattern))
    for y in range(0, brick_lines):
        for x in range(0, brick_cols):
            display(w, (x * len(brick_std_pattern), y, brick_std_pattern))
    w.refresh()
    while True:
        if count_bricks(brick_states) == 0:
            display(w, (curses.COLS / 2, curses.LINES / 2, "YOU WON"))
            break
        key = w.getch()
        if key == curses.KEY_LEFT:
            erase(w, (paddle_x, paddle_y, paddle_pattern))
            paddle_x = max(paddle_x - paddle_speed, 0)
        if key == curses.KEY_RIGHT:
            erase(w, (paddle_x, paddle_y, paddle_pattern))
            paddle_x = min(paddle_x + paddle_speed, curses.COLS - len(paddle_pattern))
        erase(w, (ball_x, ball_y, ball_pattern))
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        if ball_x <= 0:
            ball_x = 0
            ball_speed_x = -ball_speed_x
        if ball_x >= curses.COLS - 1:
            ball_x = curses.COLS - 1
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_y = 0
            ball_speed_y = -ball_speed_y
        if int(ball_y) == paddle_y:
            if int(ball_x) in range(paddle_x, paddle_x + len(paddle_pattern)):
                half_paddle_length = len(paddle_pattern) // 2
                ball_speed_x *= 3 * (ball_x - (paddle_x + half_paddle_length)) / half_paddle_length
                ball_speed_y = -ball_speed_y
            else:
                display(w, (curses.COLS / 2, curses.LINES / 2, "GAME OVER"))
                break
        elif int(ball_y) in range(0, brick_lines):
            brick_x = int(ball_x) // len(brick_std_pattern)
            brick_y = int(ball_y)
            if brick_x in range(0, brick_cols) and brick_states[brick_y][brick_x]:
                erase(w, (brick_x * len(brick_std_pattern), brick_y, brick_std_pattern))
                brick_states[brick_y][brick_x] = False
                ball_speed_y = -ball_speed_y
        display(w, (ball_x, ball_y, ball_pattern))
        display(w, (paddle_x, paddle_y, paddle_pattern))
        # debug(w, ball_x, ball_y, ball_speed_x, ball_speed_y, brick_states)
        w.refresh()
    w.nodelay(False)
    w.getch()


if __name__ == "__main__":
    wrapper(main)
