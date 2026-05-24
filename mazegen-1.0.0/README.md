*This project has been created as part of the 42 curriculum by spujol-s, esucarra*

# A-Maze-ing

## Description

A-Maze-ing is a visual Python maze generator and solver.

Project goals:
- Generate a valid maze from a configuration file (config.txt).
- Support perfect and imperfect mazes.
- Save the generated maze using a hexadecimal base.
- Display the shortest valid path from entry to exit.
- Provide interactive terminal controls (regenerate, show/hide path, color rotation).

Current implementation overview:
- Main entry point: a_maze_ing.py.
- Config parsing and validation: create_config.py (Pydantic-based).
- Reusable maze logic class: maze_gen.py (MazeGenerator).

## Instructions

### Requirements

- Python 3.10+
- make

### Install

```bash
make install
```

This command creates venv (if missing), upgrades pip, installs the package in editable mode, and installs lint tools.

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

Validation rules enforced by the project:
- Mandatory keys must exist.
- No duplicate keys.
- ENTRY and EXIT must be inside bounds.
- ENTRY and EXIT must be different.
- OUTPUT_FILE must end with .txt and cannot contain '/'.

## Maze Generation Algorithm

Chosen algorithm:
- Randomized depth-first search (recursive backtracker style, implemented iteratively with a stack).

Why this algorithm:
- Simple and reliable for generating connected mazes.
- Naturally produces perfect mazes (single path between two cells) when no extra walls are removed.
- Easy to extend with a post-process step to create imperfect mazes.
- Good fit for readable, reusable class-based Python code.

Imperfect mode:
- After generating a perfect maze, extra walls are removed in selected cells to create additional paths.

Pathfinding:
- Breadth-first search (BFS) is used to compute a shortest valid path from ENTRY to EXIT.

## Maze Requirements Coverage

Implemented:
- Random generation.
- Optional reproducibility via SEED.
- Border constraints and coherent wall encoding.
- Entry/exit validation.
- Optional perfect maze generation.
- Visible "42" pattern using blocked cells when maze size allows it.
- Terminal visualization with path and color interactions.

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

This project currently provides terminal rendering.

Interactive options:
- Regenerate maze
- Show/Hide shortest path
- Rotate maze color theme
- Quit

## Reusability

Reusable component:
- MazeGenerator class in maze_gen.py

How to use it:

```python
from maze_gen import MazeGenerator

maze = MazeGenerator(width=20, height=15, perfect=True)
maze.sign_42()
maze.generate()
path = maze.solve_bfs((0, 0), (19, 14))
maze.save_to_file("maze.txt", (0, 0), (19, 14))
```

What can be reused:
- Maze generation logic.
- BFS path computation.
- Path coordinates extraction.
- File export in project format.
- Terminal rendering helper methods.

## Team and Project Management

Team members:
- spujol-s
- esucarra

Roles:
- Both members contributed to algorithm, implementation, testing, and project setup.

Planned workflow:
- Define config format and data validation first.
- Implement generation and file output second.
- Add rendering and interactive controls third.
- Finalize with linting and packaging.

How it evolved:
- Validation and error handling required more iteration than expected.
- Visualization details (colors/path clarity) were refined late in development.

What worked well:
- Clear module split (entry/config/generator).
- Fast iteration with Makefile targets.

What could be improved:
- Add automated tests (pytest/unittest) for edge cases.
- Increase type coverage in utility/test scripts.
- Expand documentation with example screenshots.

Tools used:
- Python 3.10+
- Pydantic
- flake8
- mypy
- make
- venv

## Resources

Classic references:
- Python documentation: https://docs.python.org/3/
- Pydantic documentation: https://docs.pydantic.dev/
- BFS overview: https://en.wikipedia.org/wiki/Breadth-first_search
- Maze generation (recursive backtracker): https://en.wikipedia.org/wiki/Maze_generation_algorithm

AI usage in this project:
- Used AI for repetitive writing and formatting tasks (README drafting and section structuring).
- Used AI for review support (spotting lint and typing gaps).
- All generated content was manually reviewed, adapted, and validated before use.

## Repository Structure

- a_maze_ing.py: main interactive program
- create_config.py: config parsing and validation
- maze_gen.py: reusable maze module
- config.txt: default configuration file
- Makefile: install/run/debug/lint/clean automation
- pyproject.toml: package metadata and dependencies
