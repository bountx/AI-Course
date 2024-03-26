# Import necessary libraries
from typing import List, Tuple, Optional
import numpy as np

# Define constants for cell states
UNKNOWN = -1
EMPTY = 0
FILLED = 1

# Solution class (adapted and simplified from solution.py, without visualization)
class Solution:
    def __init__(self, row_rules: List[List[int]], col_rules: List[List[int]]):
        self.row_rules = row_rules
        self.col_rules = col_rules
        self.rows = len(row_rules)
        self.cols = len(col_rules)
        self.board = np.full((self.rows, self.cols), UNKNOWN, dtype=int)
    
    def is_solved(self) -> bool:
        return not (self.board == UNKNOWN).any()
    
    def apply_move(self, row: int, col: int, state: int):
        self.board[row, col] = state
    
    def is_valid(self) -> bool:
        # Simplified validity check, excluding visualization-dependent logic
        # This function should be expanded based on specific rule checks
        return True

# Solver class (combined and adapted from solver.py, without visualization logic)
class Solver:
    def __init__(self, solution: Solution):
        self.solution = solution
    
    def solve(self):
        # Attempt to solve the puzzle by applying the rules iteratively
        if apply_rules(self.solution):
            print("Puzzle solved successfully!")
        else:
            print("Could not solve the puzzle. More sophisticated rules or guesswork may be needed.")

def rule1(solution: Solution) -> bool:
    changed = False
    for i, row in enumerate(solution.row_rules):
        num_blocks = len(row)
        if num_blocks == 0:
            for j in range(solution.cols):
                if solution.board[i, j] != EMPTY:
                    solution.apply_move(i, j, EMPTY)
                    changed = True
        else:
            min_length = sum(row) + num_blocks - 1
            if min_length == solution.cols:
                cursor = 0
                for block in row:
                    for _ in range(block):
                        if solution.board[i, cursor] != FILLED:
                            solution.apply_move(i, cursor, FILLED)
                            changed = True
                        cursor += 1
                    if cursor < solution.cols:
                        if solution.board[i, cursor] != EMPTY:
                            solution.apply_move(i, cursor, EMPTY)
                            changed = True
                        cursor += 1
    return changed

# Implementing Rule 2 based on the provided GitHub link

def rule2(solution: Solution) -> bool:
    changed = False
    
    # Function to find all possible permutations of blocks in a line
    def find_permutations(line, blocks, index=0, start=0):
        if index == len(blocks):
            yield line[:]
        else:
            for i in range(start, len(line) - sum(blocks[index:]) - len(blocks) + index + 2):
                new_line = line[:]
                for j in range(blocks[index]):
                    new_line[i + j] = FILLED
                if index < len(blocks) - 1:
                    new_line[i + blocks[index]] = EMPTY
                yield from find_permutations(new_line, blocks, index + 1, i + blocks[index] + 1)
    
    # Apply permutations to rows
    for i, row in enumerate(solution.row_rules):
        if not row:
            continue
        line = [UNKNOWN] * solution.cols
        permutations = list(find_permutations(line, row))
        
        # Find common cells in all permutations
        common_filled = [j for j in range(solution.cols) if all(p[j] == FILLED for p in permutations)]
        common_empty = [j for j in range(solution.cols) if all(p[j] == EMPTY for p in permutations)]
        
        # Apply moves based on common cells
        for j in common_filled:
            if solution.board[i, j] != FILLED:
                solution.apply_move(i, j, FILLED)
                changed = True
        for j in common_empty:
            if solution.board[i, j] != EMPTY:
                solution.apply_move(i, j, EMPTY)
                changed = True
    
    # The same logic can be applied to columns by transposing the board,
    # but this requires adapting the solution class or handling in a different manner
    
    return changed


def rule3(solution: Solution) -> bool:
    changed = False

    def overlap_for_line(line, blocks):
        line_length = len(line)
        possible_starts = [0] * len(blocks)
        possible_ends = [0] * len(blocks)

        # Calculate possible start and end positions for each block
        position = 0
        for i, block in enumerate(blocks):
            while position < line_length and line[position] == EMPTY:
                position += 1
            possible_starts[i] = position
            position += block
            possible_ends[i] = position
            position += 1  # Skip at least one cell for the next block

        # Adjust possible ends by moving backwards
        position = line_length
        for i in range(len(blocks) - 1, -1, -1):
            block = blocks[i]
            position -= 1
            while position >= 0 and line[position] == EMPTY:
                position -= 1
            possible_ends[i] = min(possible_ends[i], position + 1)
            position -= block
            possible_starts[i] = max(possible_starts[i], position - block + 1)

        return possible_starts, possible_ends

    # Apply overlap logic to rows
    for i, blocks in enumerate(solution.row_rules):
        if blocks:
            line = solution.board[i]
            possible_starts, possible_ends = overlap_for_line(line, blocks)
            for block_index, block in enumerate(blocks):
                for j in range(possible_starts[block_index], possible_ends[block_index] - block + 1):
                    if line[j] != FILLED:
                        solution.apply_move(i, j, FILLED)
                        changed = True

    # Similar logic can be applied to columns, but you might need to transpose or adapt the approach

    return changed


# Combine rule application in the solving process
def apply_rules(solution: Solution) -> bool:
    # This function applies all rules iteratively until no more changes occur or the puzzle is solved.
    changed = True
    while changed and not solution.is_solved():
        changed = False
        # Apply each rule in sequence and check if any changes were made.
        for rule in (rule1, rule2, rule3):
            if rule(solution):
                changed = True
                break  # Break after any rule makes a change, and start the sequence again.
    return solution.is_solved()

example_input = """
9 9
1 1 1
5 1
1 1 1 1
5 1
6 1
7
6
1 3
2 4
4
1 2 1
8
1 4
7 1
5
5
4
6
"""

solution = Solution([[1, 1, 1], [5, 1], [1, 1, 1, 1], [5, 1], [6, 1], [7], [6], [1, 3], [2, 4]],
                    [[4], [1, 2, 1], [8], [1, 4], [7, 1], [5], [5], [4], [6]])
solver = Solver(solution)
solver.solve()

for row in solution.board:
    print("".join("#" if cell == FILLED else "." for cell in row))