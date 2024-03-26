import heapq
from collections import deque

class MazeSolverAStarWithCostCheck:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        self.start_positions = frozenset((x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'S' or maze[x][y] == 'B')
        self.end_positions = frozenset((x, y) for x in range(self.height) for y in range(self.width) if maze[x][y] == 'B' or maze[x][y] == 'G')
        self.costs = {(x, y) : 0 for x in range(self.height) for y in range(self.width)}

    def distance_bfs(self, position):
        queue = deque([(position, 0)])
        visited = {position}
        distance = 0
        while queue:
            for _ in range(len(queue)):
                (x, y), distance = queue.popleft()
                if (x, y) in self.end_positions:
                    return distance
                for dx, dy in self.directions.values():
                    new_x, new_y = x + dx, y + dy
                    if (self.maze[new_x][new_y] != '#' and(new_x, new_y) not in visited):
                        queue.append(((new_x, new_y), distance + 1))
                        visited.add((new_x, new_y))
        return distance

    def calculate_costs(self):
        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):
                self.costs[(x, y)] = self.distance_bfs((x, y))
            

    def is_end_state(self, positions):
        return all(pos in self.end_positions for pos in positions)

    def solve_with_a_star(self):
        queue = []
        visited = set()
        start_cost = max(self.costs[pos] for pos in self.start_positions)
        heapq.heappush(queue, (0, start_cost, "", self.start_positions))

        while queue:
            _,steps, path, positions = heapq.heappop(queue)
            if self.is_end_state(positions):
                return path
            for direction_key, (dx, dy) in self.directions.items():
                new_positions = set()
                new_cost = 0
                for x, y in positions:
                    new_x, new_y = x + dx, y + dy
                    if self.maze[new_x][new_y] != '#':
                        new_positions.add((new_x, new_y))
                        new_cost = max(new_cost, self.costs[(new_x, new_y)])
                    else:
                        new_positions.add((x, y))
                        new_cost = max(new_cost, self.costs[(x, y)])
                new_positions = frozenset(new_positions)
                if new_positions in visited:
                    continue
                visited.add(new_positions)
                new_cost += steps
                heapq.heappush(queue, (new_cost, steps + 1, path + direction_key, new_positions))
        

file = open("zad_input.txt", "r")
maze = [line.strip() for line in file]
file.close()

solver = MazeSolverAStarWithCostCheck(maze)
solver.calculate_costs()
solution = solver.solve_with_a_star()

file = open("zad_output.txt", "w")
file.write(solution)
file.close()
