from typing import Optional
from create_config import Config, ConfigError, create_config
from package.mazegen import MazeGenerator
from maze_display import display
import os
import random
import sys
import time


def get_seed(maze: MazeGenerator, config: Config) -> int:
    """
    Return the configured seed or generate a random one.
    """
    if config.seed is not None:
        return config.seed
    if maze.seed is None:
        raise ValueError("Maze seed is unexpectedly None")
    return maze.seed


def generate_maze(
    config: Config, current_seed: Optional[int]
) -> tuple[MazeGenerator, bool]:
    """
    Build, generate and save a maze for the given seed.
    Returns the maze object to display it and if it has the '42' sign.
    """
    random.seed(current_seed)
    maze = MazeGenerator(config.width, config.height,
                         config.perfect, current_seed)
    has_42 = maze.sign_42()

    def relocate_point(maze: MazeGenerator, point: tuple[int, int]
                       ) -> tuple[int, int]:
        x, y = point
        candidates = []
        if maze.maze[y][x - 1] != -1:
            candidates.append((x - 1, y))
        if maze.maze[y][x + 1] != -1:
            candidates.append((x + 1, y))
        if maze.maze[y - 1][x] != -1:
            candidates.append((x, y - 1))
        if maze.maze[y + 1][x] != -1:
            candidates.append((x, y + 1))
        selected = random.choice(candidates)
        return selected

    if maze.maze[config.entry[1]][config.entry[0]] == -1:
        new_entry = relocate_point(maze, config.entry)
        print(
            f"ENTRY landed inside the 42 pattern. Moving it from "
            f"{config.entry} to {new_entry}."
        )
        input("Press Enter to continue...")
        config.entry = new_entry

    if maze.maze[config.exit[1]][config.exit[0]] == -1:
        new_exit = relocate_point(maze, config.exit)
        print(
            f"EXIT landed inside the 42 pattern. Moving it from "
            f"{config.exit} to {new_exit}"
        )
        input("Press Enter to continue...")
        config.exit = new_exit
    maze.generate()
    maze.save_to_file(config.output_file, config.entry, config.exit)
    return maze, has_42


def render_screen(maze: MazeGenerator, config: Config, show_path: bool,
                  colours: dict[str, str], has_42: bool) -> None:
    """
    Clear the terminal and render the current maze state.
    """
    os.system("clear")
    print(f"Actual theme: {colours['name']}")
    print(f"Using SEED: {get_seed(maze, config)}")
    display(maze, config.entry, config.exit, show_path, colours)
    if not has_42:
        print("Maze is too small for the '42' sign. Skipping it.")
    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Theme gambling")
    print("5. Quit")


def theme_gambling(maze: MazeGenerator, config: Config, show_path: bool,
                   themes: list[dict[str, str]], has_42: bool,
                   current_theme: int) -> int:
    """
    Render the maze with a simple roulette effect in 3 phases.
    """
    phases = [
        (11, 0.08),
        (8, 0.16),
        (6, 0.32),
        (3, 0.8)
    ]
    for steps, delay in phases:
        for _ in range(steps):
            current_theme = (current_theme + 1) % len(themes)
            colours = themes[current_theme]
            render_screen(
                maze, config, show_path, colours, has_42
            )
            time.sleep(delay)
    return current_theme


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_path = sys.argv[1]
    try:
        config = create_config(config_path)
        themes = [
            {'name': 'Basic', 'wall': 'white', 'way': 'black',
             '42': 'grey', 'path': 'cyan'},
            {'name': 'Barca', 'wall': 'red-blue', 'way': 'black',
             '42': 'white', 'path': 'cyan'},
            {'name': 'Hell', 'wall': 'red', 'way': 'black',
             '42': 'yellow', 'path': 'white'},
            {'name': 'Barbie', 'wall': 'pink', 'way':
             'white', '42': 'yellow', 'path': 'cyan'},
            {'name': 'Noise', 'wall': 'b_random', 'way':
             'w_random', '42': 'blue', 'path': 'yellow'},
            {'name': 'Exotic', 'wall': 'red-pink', 'way':
             'white', '42': 'black', 'path': 'b_random'},
            {'name': 'WTF...', 'wall': 'random', 'way':
             'white', '42': 'black', 'path': 'red'},
            {'name': 'Legendary', 'wall': 'black', 'way':
             'white-yellow', '42': 'yellow', 'path': 'blue'},
            {'name': 'Jungle', 'wall': 'green-blue', 'way':
             'red-yellow', '42': 'black', 'path': 'white'},
            {'name': 'Gold chest', 'wall': 'black-yellow', 'way':
             'white-yellow', '42': 'red', 'path': 'blue'},
            {'name': 'Shit', 'wall': 'black', 'way':
             'brown', '42': 'white', 'path': 'grey'}
        ]
        show_path, current_theme = True, 0

        maze, has_42 = generate_maze(config, config.seed)

        while True:
            colours = themes[current_theme]
            render_screen(maze, config, show_path, colours, has_42)
            choice = input("Choice? (1-5): ")

            if choice == "1":
                maze, has_42 = generate_maze(config, config.seed)
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                current_theme = (current_theme + 1) % len(themes)
            elif choice == "4":
                current_theme = theme_gambling(maze, config, show_path,
                                               themes, has_42,
                                               current_theme)
            elif choice == "5":
                break
            else:
                input("Invalid option. Press Enter to continue...")
    except ConfigError as ce:
        print(f"ConfigError: {ce}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
