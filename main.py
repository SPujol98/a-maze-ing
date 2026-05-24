from mazegen import MazeGenerator

maze = MazeGenerator(width=20, height=15, perfect=True)
maze.sign_42()
maze.generate()
path = maze.solve_bfs((0, 0), (19, 14))
maze.save_to_file("maze.txt", (0, 0), (19, 14))