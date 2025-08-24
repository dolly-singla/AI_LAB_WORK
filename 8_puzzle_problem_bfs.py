import copy
from collections import deque  

class State:
    _id_counter = 0

    def __init__(self, puzzle, parent_id=None):
        self.puzzle = puzzle
        self.parent_id = parent_id
        self.state_id = State._id_counter
        State._id_counter += 1

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.puzzle])

    def find_blank(self):
        for r in range(3):
            for c in range(3):
                if self.puzzle[r][c] == 0:
                    return r, c

    def get_possible_moves(self):
        moves = []
        row, col = self.find_blank()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_puzzle = copy.deepcopy(self.puzzle)
                new_puzzle[row][col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[row][col]
                new_state = State(new_puzzle, parent_id=self.state_id)
                moves.append(new_state)

        return moves

    def puzzle_to_tuple(self):
        return tuple(tuple(row) for row in self.puzzle)


class PuzzleSolver:
    def __init__(self, start_puzzle, goal_puzzle):
        self.start_state = State(start_puzzle)
        self.goal_puzzle = goal_puzzle
        self.closed = set()  # Visited/Closed states
        self.queue = deque([self.start_state])  #  BFS queue
        self.state_map = {self.start_state.state_id: self.start_state}
        self.visited_states = []

    def solve(self):
        print("\n🔸 Goal State:")
        print(self.format_puzzle(self.goal_puzzle))
        print("=" * 20)

        while self.queue:
            current = self.queue.popleft()  
            current_key = current.puzzle_to_tuple()

            if current_key in self.closed:
                continue

            self.closed.add(current_key)
            self.visited_states.append(current)

            if current.puzzle == self.goal_puzzle:
                print("\n Goal reached!\n")
                self.print_all_visited_states()
                self.print_final_path(current.state_id)
                return

            for neighbor in current.get_possible_moves():
                if neighbor.puzzle_to_tuple() not in self.closed:
                    self.queue.append(neighbor)
                    self.state_map[neighbor.state_id] = neighbor

        print(" No solution found.")

    def format_puzzle(self, puzzle):
        return "\n".join([" ".join(map(str, row)) for row in puzzle])

    def print_all_visited_states(self):
        print("\n🔹 BFS Traversal Path (Visited States in Order):\n")
        for i, state in enumerate(self.visited_states):
            print(f"Visited State {i} - State ID: {state.state_id}, Parent ID: {state.parent_id}")
            print(state)
            print("-" * 20)

    def print_final_path(self, goal_id):
        path = []
        while goal_id is not None:
            state = self.state_map[goal_id]
            path.append(state)
            goal_id = state.parent_id

        path.reverse()
        print("\n🎯 Final Path from Start to Goal:")
        print(f"Path Length: {len(path)}\n")
        for i, state in enumerate(path):
            print(f"Step {i} - State ID: {state.state_id}, Parent ID: {state.parent_id}")
            print(state)
            print("-" * 20)


def take_user_input():
    print("Enter the 8-puzzle start state (use 0 for the blank tile):")
    start = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1} : ").strip().split()))
        assert len(row) == 3, "Each row must contain exactly 3 numbers."
        start.append(row)
    return start


if __name__ == "__main__":
    start_puzzle = take_user_input()

    goal_puzzle = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    solver = PuzzleSolver(start_puzzle, goal_puzzle)
    solver.solve()
