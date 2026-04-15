*This project has been created as part of the 42 curriculum by spujol-s, esucarra*

# A-Maze-ing

## Description

A-Maze-ing is a visual Python maze generator and solver.

Project goals:
- Generate a valid maze from a configuration file (config.txt).
- Support perfect and imperfect mazes.
- Save the generated maze information using a hexadecimal base and the solution path.
- Provide interactive terminal controls (regenerate, show/hide path, color rotation, theme gambling).

Current implementation:
- Main Python script: a_maze_ing.py.
- Config parsing and validation: create_config.py (validated with Pydantic).
- Reusable maze logic class: package/mazegen.py (MazeGenerator).
- Maze visualization: maze_display.py

## Instructions

### Requirements

- Python 3.10+
- make

### Install

```bash
make install
```

This command creates `venv` if needed, upgrades pip, and installs the project dependencies from `requirements.txt`.

### Lint

```bash
make lint
make lint-strict
```

### Run

```bash
make run
```

Equivalent:

```bash
python3 a_maze_ing.py config.txt
```

### Debug

```bash
make debug
```

### Clean

```bash
make clean
```

## Configuration File Format

The configuration file uses one KEY=VALUE per line.
Lines starting with # are ignored.

Mandatory keys:
- WIDTH: maze width in cells (int, >1 and <999)
- HEIGHT: maze height in cells (int, >1 and <999)
- ENTRY: entry coordinates (x,y)
- EXIT: exit coordinates (x,y)
- OUTPUT_FILE: output file name ending in .txt (filename only, no path)
- PERFECT: boolean (true/false, yes/no, on/off, 1/0)

Optional keys:
- SEED: integer seed for reproducible generation

Default config example:

```txt
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=12,14
OUTPUT_FILE=output.txt
PERFECT=no
#SEED=874013
```

## Maze Generation Algorithm

Chosen algorithm:
- Recursive backtracking, implemented iteratively with a stack.

Why this algorithm:
- Simple and reliable for generating good-looking mazes.
- Naturally produces perfect mazes (single path between two cells) when no extra walls are removed.
- Easy to extend to an imperfect maze.

Imperfect mode:
- After generating a perfect maze, dead-end walls are removed randomly to create additional paths.

Pathfinding:
- Breadth-first search (BFS) is used to compute a shortest valid path from ENTRY to EXIT.

## Maze Requirements Coverage

Implemented:
- Can be reproducible via SEED or use a randomized seed.
- Entry/exit validation.
- Visible "42" pattern when the size allows it.

Behavior for small mazes:
- If the maze is too small for the "42" pattern, the program prints a message.

## Output File Format

Each cell is encoded as one hexadecimal digit where wall bits are:
- bit 0: North
- bit 1: East
- bit 2: South
- bit 3: West

File structure:
1. Maze rows in hex (one row per line).
2. One empty line.
3. ENTRY coordinates: x,y
4. EXIT coordinates: x,y
5. Shortest path string using N/E/S/W

All lines end with \n.

## Visual Representation

This project provides terminal rendering.

Interactive options:
- Regenerate maze
- Show/Hide shortest path
- Rotate maze color theme
- Get a random color theme with an animation
- Quit

## Reusability

Reusable component:
- MazeGenerator class in package/mazegen.py

First the mazegen...tar needs to be installed with pip install.

Then it can be used with:

```python
from mazegen import MazeGenerator
```

Example usage:

```python
maze = MazeGenerator(width=20, height=15, perfect=True, seed_number=1234)
maze.sign_42()
maze.generate()
```

What can also be reused:
- BFS path computation.
- Path coordinates extraction.
- File export in project format.

Parameters for all mazes:
- `width` and `height` define maze size.
- `perfect` toggles perfect vs imperfect generation.
- `seed_number` fixes the random seed for reproducible output.

Functions with more parameters (entry, exit):
- `maze.solve_bfs(start, end)` returns the shortest valid path as a string.
- `maze.get_path_coords(start, path_str)` converts a solution into visited coordinates.

## Team and Project Management

Team members:
- spujol-s
- esucarra

Roles:
- Both members contributed to algorithm, implementation, testing, and project setup,
    and worked together for the most part.

Planned workflow:
1. Define config format and data validation first.
2. Implement generation and file output second.
3. Add rendering and interactive controls third.
4. Make the packaging and reusability possible.
5. Check for general errors in the code.

How it evolved:
- It evolved quickly, brick by brick, and before we realized it, everything was finished.

What worked well:
- Doing each step of the project properly before moving to the next one.

What could be improved:
- More organized code in some aspects.
- Expand documentation with example screenshots.

Tools used:
- Python 3.10+
- Pydantic
- flake8
- mypy
- make
- venv
- build

## Resources

Basic resources:
- Pydantic: learned by doing module 09 of the Python modules.
- BFS and recursive backtracking: videos from the internet and some colleagues that helped us understand.

AI usage in this project:
- Used AI for repetitive writing and formatting tasks, for example changing a variable name everywhere quickly.
- Used AI to review the code after our own verification.
- All generated content was manually reviewed, adapted, and validated before use.

## Repository Structure

- a_maze_ing.py
- create_config.py
- package/mazegen.py
- package/README.md: documentation
- config.txt
- Makefile: install/run/debug/lint/clean
- pyproject.toml: to create the reusable module
