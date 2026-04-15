## MazeGenerator

`MazeGenerator` is the reusable maze engine used by the project.

### Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, perfect=True, seed_number=42)
maze.sign_42()
maze.generate()
maze.save_to_file("maze.txt", (0, 0), (19, 14))
```

### Parameters

- `width`: maze width in cells.
- `height`: maze height in cells.
- `perfect`: generates a perfect maze when `True`.
- `seed_number`: optional seed for reproducible results.

### Available data and helpers

- `maze.maze`: raw maze grid using hexadecimal wall encoding.
- `maze.generate()`: builds the maze.
- `maze.sign_42()`: inserts the visible `42` pattern when the size allows it.
- `maze.solve_bfs(start, end)`: returns the shortest path between two cells.
- `maze.get_path_coords(start, path_str)`: converts a path string into visited coordinates.
- `maze.save_to_file(filename, entry, exit_coords)`: writes the maze using the subject format.
