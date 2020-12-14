from typing import Tuple, List, Set, Optional
import random

def read_sudoku(filename: str) -> List[List[str]]:
    #Прочитать Судоку из указанного файла
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid

def group(values: List[str], n: int) -> List[List[str]]:
    #Сгруппировать значения values в список, состоящий из списков по n элементов
    return [values[i : i + n] for i in range(0, len(values), n)]

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    #Возвращает все значения для номера строки, указанной в pos
    return grid[pos[0]]

def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    #Возвращает все значения для номера столбца, указанного в pos
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    #Возвращает все значения из квадрата, в который попадает позиция pos
    row, col = pos
    br = 3 * (row // 3)
    bc = 3 * (col // 3)
    return [grid[br + i][bc + j] for i in range(3) for j in range(3)]

def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    # Решение пазла, заданного в grid
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, column = pos
    for value in find_possible_values(grid, pos):
        grid[row][column] = value
        solution = solve(grid)
        if solution:
            return solution
    grid[row][column] = "."
    return None

def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    #Найти первую свободную позицию в пазле
    for i in range(len(grid)):
        for l in range(len(grid)):
            if grid[i][l] == ".":
                return i, l
    return None

def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    #Вернуть множество возможных значения для указанной позиции
    return (
        set("123456789")
        - set(get_row(grid, pos))
        - set(get_col(grid, pos))
        - set(get_block(grid, pos))
    )

def check_solution(solution: List[List[str]]) -> bool:
    # Если решение solution верно, то вернуть True, в противном случае False
    for row in range(len(solution)):
        values = set(get_row(solution, (row, 0)))
        if values != set("123456789"):
            return False

    for column in range(len(solution)):
        values = set(get_col(solution, (0, column)))
        if values != set("123456789"):
            return False

    for row in (0, 3, 6):
        for column in (0, 3, 6):
            values = set(get_block(solution, (row, column)))
            if values != set("123456789"):
                return False

    return True

def generate_sudoku(N: int) -> List[List[str]]:
    #Генерация судоку заполненного на N элементов
    grid = solve([["."] * 9 for _ in range(9)])  # type: ignore
    N = 81 - min(81, N)
    while N:
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        if grid is not None:
            if grid[row][column] != ".":
                grid[row][column] = "."
                N -= 1
    return grid

def display(grid: List[List[str]]) -> None:
    #Вывод Судоку
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()

if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
