import random
from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        # Map directions to tuples and corresponding characters for easier tracking
        self.directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        self.direction_chars = {(-1, 0): 'U', (1, 0): 'D', (0, -1): 'L', (0, 1): 'R'}
        self.start_positions = {(x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'S'}
        self.end_positions = {(x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'B'}
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
        min_positions = len(self.start_positions)
        queue = deque([(self.start_positions, "")])
        self.visited.add(frozenset(self.start_positions))
        while queue:
            positions, path = queue.popleft()
            if self.is_end_state(positions):
                return self.moves_taken + path  # Include pre-BFS moves
            for direction_key, (dx, dy) in self.directions.items():
                new_positions = set()
                for x, y in positions:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.height and 0 <= new_y < self.width and self.maze[new_x][new_y] != '#':
                        new_positions.add((new_x, new_y))
                    else:
                        new_positions.add((x, y))
                new_positions_frozen = frozenset(new_positions)
                if new_positions_frozen not in self.visited:
                    self.visited.add(new_positions_frozen)
                    queue.append((new_positions, path + direction_key))  # Append the move to the path
        return "No solution found."

    def is_end_state(self, positions):
        return all(pos in self.end_positions for pos in positions)

    def check_answer(self, start_positions, moves):
        current_positions = start_positions.copy()
        for move in moves:
            new_positions = set()
            direction = self.directions[move]
            for x, y in current_positions:
                new_x, new_y = x + direction[0], y + direction[1]
                # Check bounds and wall collisions
                if 0 <= new_x < self.height and 0 <= new_y < self.width and self.maze[new_x][new_y] != '#':
                    new_positions.add((new_x, new_y))
                else:
                    # If a move isn't valid (hits a wall), the position doesn't change.
                    new_positions.add((x, y))
            current_positions = new_positions

        # After applying all moves, check if all current positions are in end positions.
        return all(pos in self.end_positions for pos in current_positions)

file = open("zad_input.txt", "r")
maze = [line.strip() for line in file]
file.close()

solver = MazeSolver(maze)
start_po = solver.start_positions
solver.reduce_positions()
solution = solver.solve_with_bfs()

file = open("zad_output.txt", "w")
file.write(solution)
file.close()