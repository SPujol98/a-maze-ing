import random
from collections import deque


class MazeGenerator:
    def __init__(self, width: int, height: int, perfect: bool = True,
                 seed_number: int = None):
        self.width = width
        self.height = height
        self.perfect = perfect
        self.maze = [[15 for _ in range(width)] for _ in range(height)]
        self.seed = seed_number
        if seed_number is None:
            current_seed = random.randint(0, 1000000)
            self.seed = current_seed
        random.seed(self.seed)

    def generate(self) -> None:
        cell = self.maze
        x = 0
        y = 0
        visited = [(x, y)]
        while visited:
            x, y = visited[-1]
            able = {"W": False, "S": False, "E": False, "N": False}
            # can move west
            if 0 <= x - 1 < self.width and cell[y][x - 1] == 15:
                able["W"] = True
            # can move south
            if 0 <= y + 1 < self.height and cell[y + 1][x] == 15:
                able["S"] = True
            # can move east
            if 0 <= x + 1 < self.width and cell[y][x + 1] == 15:
                able["E"] = True
            # can move north
            if 0 <= y - 1 < self.height and cell[y - 1][x] == 15:
                able["N"] = True
            moves = [k for k, v in able.items() if v is True]
            # no moves available
            if len(moves) == 0:
                visited.pop()
                continue
            selected = random.choice(moves)
            # break to the west
            if selected == "W":
                self.maze[y][x] -= 8
                self.maze[y][x - 1] -= 2
                x -= 1
            # break to the south
            elif selected == "S":
                self.maze[y][x] -= 4
                self.maze[y + 1][x] -= 1
                y += 1
            # break to the east
            elif selected == "E":
                self.maze[y][x] -= 2
                self.maze[y][x + 1] -= 8
                x += 1
            # break to the north
            elif selected == "N":
                self.maze[y][x] -= 1
                self.maze[y - 1][x] -= 4
                y -= 1
            visited.append((x, y))
        if not self.perfect:
            self.make_imperfect()

    def make_imperfect(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]
                if cell == 7 or cell == 11 or cell == 13 or cell == 14:
                    able = {"W": False, "S": False, "E": False, "N": False}
                    # can break west
                    if 0 <= x - 1 and \
                       cell != 7 and self.maze[y][x - 1] != -1:
                        able["W"] = True
                    # can break south
                    if y + 1 < self.height and \
                       cell != 11 and self.maze[y + 1][x] != -1:
                        able["S"] = True
                    # can break east
                    if x + 1 < self.width and \
                       cell != 13 and self.maze[y][x + 1] != -1:
                        able["E"] = True
                    # can break north
                    if 0 <= y - 1 and \
                       cell != 14 and self.maze[y - 1][x] != -1:
                        able["N"] = True
                    moves = [k for k, v in able.items() if v is True]
                    if len(moves) == 0:
                        continue
                    selected = random.choice(moves)
                    # break to the west
                    if selected == "W":
                        self.maze[y][x] -= 8
                        self.maze[y][x - 1] -= 2
                    # break to the south
                    elif selected == "S":
                        self.maze[y][x] -= 4
                        self.maze[y + 1][x] -= 1
                    # break to the east
                    elif selected == "E":
                        self.maze[y][x] -= 2
                        self.maze[y][x + 1] -= 8
                    # break to the north
                    elif selected == "N":
                        self.maze[y][x] -= 1
                        self.maze[y - 1][x] -= 4

    def sign_42(self) -> bool:
        if self.width >= 9 and self.height >= 7:
            w_margin = (self.width - 7) // 2
            h_margin = (self.height - 5) // 2
            # Weird number 4
            self.maze[h_margin][w_margin] = -1
            self.maze[h_margin + 1][w_margin] = -1
            self.maze[h_margin + 2][w_margin] = -1
            self.maze[h_margin + 2][w_margin + 1] = -1
            self.maze[h_margin + 2][w_margin + 2] = -1
            self.maze[h_margin + 3][w_margin + 2] = -1
            self.maze[h_margin + 4][w_margin + 2] = -1
            # Number 2
            self.maze[h_margin][w_margin + 4] = -1
            self.maze[h_margin][w_margin + 5] = -1
            self.maze[h_margin][w_margin + 6] = -1
            self.maze[h_margin + 1][w_margin + 6] = -1
            self.maze[h_margin + 2][w_margin + 6] = -1
            self.maze[h_margin + 2][w_margin + 5] = -1
            self.maze[h_margin + 2][w_margin + 4] = -1
            self.maze[h_margin + 3][w_margin + 4] = -1
            self.maze[h_margin + 4][w_margin + 4] = -1
            self.maze[h_margin + 4][w_margin + 5] = -1
            self.maze[h_margin + 4][w_margin + 6] = -1
            return True
        else:
            return False

    def save_to_file(self, filename: str, entry: tuple[int, int],
                     exit_coords: tuple[int, int]) -> None:
        path = self.solve_bfs(entry, exit_coords)

        try:
            with open(filename, 'w') as f:
                for row in self.maze:
                    hex_row = "".join(f"{(cell if cell != -1 else 15):X}"
                                      for cell in row)
                    f.write(hex_row + "\n")
                f.write("\n")
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
                f.write(f"{path}\n")
        except IOError as e:
            print(f"Error al escribir el archivo: {e}")

    def solve_bfs(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        queue: deque[tuple[int, int, str]] = deque([(start[0], start[1], "")])
        visited: set[tuple[int, int]] = {start}

        moves = [(0, -1, 'N', 1),
                 (1, 0, 'E', 2),
                 (0, 1, 'S', 4),
                 (-1, 0, 'W', 8)]

        while queue:
            x, y, path = queue.popleft()
            if (x, y) == end:
                return path
            for dx, dy, direction, bit in moves:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if ((self.maze[y][x] & bit) == 0 and (nx, ny)
                            not in visited):
                        if self.maze[ny][nx] != -1:
                            visited.add((nx, ny))
                            queue.append((nx, ny, path + direction))
        return ""

    def get_path_coords(self, start: tuple[int, int],
                        path_str: str) -> set[tuple[int, int]]:
        coords = {start}
        x, y = start
        moves = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

        for direction in path_str:
            dx, dy = moves[direction]
            x += dx
            y += dy
            coords.add((x, y))
        return coords
