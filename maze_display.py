from random import choice
from package.mazegen import MazeGenerator


def color_to_rgb(color_name: str) -> tuple[int, int, int]:
    rgb_col = {
        "red": (255, 0, 0),
        "grey": (128, 128, 128),
        "gray": (128, 128, 128),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "magenta": (255, 0, 255),
        "pink": (255, 140, 170),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
    }
    return rgb_col.get(color_name.lower(), rgb_col["white"])


def gradient_block(maze: MazeGenerator, spec: str, x: int, y: int) -> str:
    start_name, end_name = map(str.strip, spec.split("-", 1))
    r1, g1, b1 = color_to_rgb(start_name)
    r2, g2, b2 = color_to_rgb(end_name)

    total_cells = max(1, maze.width * maze.height)
    max_index = max(1, total_cells - 1)
    index = min(y * maze.width + x, max_index)
    i = index / max_index

    red = int(r1 + i * (r2 - r1))
    green = int(g1 + i * (g2 - g1))
    blue = int(b1 + i * (b2 - b1))
    return f"\033[48;2;{red};{green};{blue}m  \033[0m"


def create_block(maze: MazeGenerator, col: str, x: int = 0, y: int = 0) -> str:
    color_str = col.strip().lower()
    if "-" in color_str and color_str != "random":
        return gradient_block(maze, color_str, x, y)

    color_codes = {
        "red": "\033[48;5;196m  \033[0m",
        "grey": "\033[48;5;240m  \033[0m",
        "brown": "\033[48;5;94m  \033[0m",
        "green": "\033[48;5;46m  \033[0m",
        "blue": "\033[48;5;21m  \033[0m",
        "yellow": "\033[48;5;226m  \033[0m",
        "magenta": "\033[48;5;201m  \033[0m",
        "pink": "\033[48;5;218m  \033[0m",
        "cyan": "\033[48;5;51m  \033[0m",
        "white": "\033[48;5;15m  \033[0m",
        "black": "\033[48;5;0m  \033[0m",
        "random": f"\033[48;5;{choice(range(17, 256))}m  \033[0m",
        "w_random": f"\033[48;5;{choice(range(249, 255))}m  \033[0m",
        "b_random": f"\033[48;5;{choice(range(232, 240))}m  \033[0m",
    }
    return color_codes.get(color_str, color_codes["white"])


def display(maze: MazeGenerator, entry: tuple[int, int], exit: tuple[int, int],
            show_path: bool, colours: dict[str, str]) -> None:
    pos = maze.maze

    def block(color: str, x: int = 0, y: int = 0) -> str:
        return create_block(maze, color, x, y)

    s42 = colours["42"]
    path_color = colours["path"]
    wall = colours["wall"]
    way = colours["way"]

    if show_path:
        path_str = maze.solve_bfs(entry, exit)
        path_coords = maze.get_path_coords(entry, path_str)
    else:
        path_coords = set()
    # North border
    for x in range(maze.width):
        print(block(wall, x, 0) * 2, end="")
    print(block(wall, maze.width - 1, 0))

    y = 0
    for row_n in range(maze.height * 2):
        # West border
        print(block(wall, 0, y), end="")
        if row_n % 2 == 1:
            # Wall row
            for x in range(maze.width):
                # South wall
                is_path_south = (
                    (x, y) in path_coords
                    and (x, y + 1) in path_coords
                    and (pos[y][x] & 4 == 0)
                )
                if is_path_south:
                    print(block(path_color, x, y), end="")
                elif pos[y][x] & 4 == 0 and pos[y][x] != -1:
                    print(block(way, x, y), end="")
                else:
                    print(block(wall, x, y), end="")
                # Corner
                print(block(wall, x, y), end="")
            print()
            y += 1
        else:
            # Way row
            for x in range(maze.width):
                # Cell
                if (x, y) == entry:
                    print(block("magenta", x, y), end="")
                elif (x, y) == exit:
                    print(block("green", x, y), end="")
                elif (x, y) in path_coords:
                    print(block(path_color, x, y), end="")
                elif pos[y][x] == -1:
                    print(block(s42, x, y), end="")
                else:
                    print(block(way, x, y), end="")

                is_path_east = (
                    (x, y) in path_coords
                    and (x + 1, y) in path_coords
                    and (pos[y][x] & 2 == 0)
                )
                # East wall
                if is_path_east:
                    print(block(path_color, x, y), end="")
                elif pos[y][x] & 2 == 0 and pos[y][x] != -1:
                    print(block(way, x, y), end="")
                else:
                    print(block(wall, x, y), end="")
            print()
