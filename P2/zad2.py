import random
from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        self.start_positions = set((x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'S' or maze[x][y] == 'B')
        self.end_positions = set((x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'B' or maze[x][y] == 'G')
        self.visited = set()
        self.moves_taken = ""  # To track the sequence of moves

    def reduce_positions(self):
        for _ in range(20): # Perform 20 "R" moves
            new_positions = set()
            for x, y in self.start_positions:
                if self.maze[x][y + 1] != '#':
                    new_positions.add((x, y + 1))
                else:
                    new_positions.add((x, y))
            self.start_positions = new_positions
            self.moves_taken += "R"
        for _ in range(20): # Perform 20 "D" moves
            new_positions = set()
            for x, y in self.start_positions:
                if self.maze[x + 1][y] != '#':
                    new_positions.add((x + 1, y))
                else:
                    new_positions.add((x, y))
            self.start_positions = new_positions
            self.moves_taken += "D"
        for _ in range(20): # Perform 20 "L" moves
            new_positions = set()
            for x, y in self.start_positions:
                if self.maze[x][y - 1] != '#':
                    new_positions.add((x, y - 1))
                else:
                    new_positions.add((x, y))
            self.start_positions = new_positions
            self.moves_taken += "L"
        for _ in range(20):  # Perform 20 "U" moves
            new_positions = set()
            for x, y in self.start_positions:
                if self.maze[x - 1][y] != '#':
                    new_positions.add((x - 1, y))
                else:
                    new_positions.add((x, y))
            self.start_positions = new_positions
            self.moves_taken += "U"
        

    def solve_with_bfs(self):
        queue = deque([(self.start_positions, self.moves_taken)])
        self.visited.add(frozenset(self.start_positions))
        while queue:
            positions, moves = queue.popleft()
            if all(pos in self.end_positions for pos in positions):
                return moves
            for direction, (dx, dy) in self.directions.items():
                new_positions = set()
                for x, y in positions:
                    new_x, new_y = x + dx, y + dy
                    if self.maze[new_x][new_y] != '#':
                        positions.add((new_x, new_y))
                    else:
                        new_positions.add((x, y))
                new_positions = frozenset(new_positions)
                if new_positions not in self.visited:
                    queue.append((new_positions, moves + direction))
                    self.visited.add(new_positions)


file = open("zad_input.txt", "r")
maze = [line.strip() for line in file]
file.close()

solver = MazeSolver(maze)
solver.reduce_positions()
print(len(solver.start_positions))
solution = solver.solve_with_bfs()

file = open("zad_output.txt", "w")
file.write(solution)
file.close()