import requests
from z3 import *


def fetch_sudoku_board() -> tuple[list[list[int]], list[list[int]]]:
    url = "https://sudoku-api.vercel.app/api/dosuku"
    response = requests.get(url)
    data = response.json()

    board = data["newboard"]["grids"][0]["value"]
    solution = data["newboard"]["grids"][0]["solution"]
    return board, solution


def draw_sudoku(board: list[list[int]]) -> None:
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            value = board[i][j]
            print(value if value != 0 else ".", end=" ")
        print()


def solve_sudoku(board: list[list[int]]) -> list[list[int]] | None:
    sudoku_vars = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]
    constraints = []

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                constraints.append(sudoku_vars[i][j] == board[i][j])

    for i in range(9):
        constraints.append(Distinct(sudoku_vars[i]))

    for j in range(9):
        constraints.append(Distinct([sudoku_vars[i][j] for i in range(9)]))

    for box_row in range(3):
        for box_col in range(3):
            box_cells = [
                sudoku_vars[i][j]
                for i in range(box_row * 3, box_row * 3 + 3)
                for j in range(box_col * 3, box_col * 3 + 3)
            ]
            constraints.append(Distinct(box_cells))

    for i in range(9):
        for j in range(9):
            constraints.append(And(sudoku_vars[i][j] >= 1, sudoku_vars[i][j] <= 9))

    solver = Solver()
    solver.add(constraints)

    if solver.check() == sat:
        model = solver.model()
        solved_board = [
            [model.evaluate(sudoku_vars[i][j]).as_long() for j in range(9)]
            for i in range(9)
        ]
        return solved_board
    else:
        return None


def main() -> None:
    board, solution = fetch_sudoku_board()
    solved_board = solve_sudoku(board)

    if solved_board:
        print("Solved Sudoku Board:")
        draw_sudoku(solved_board)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
