import numpy as np  # TODO: remove numpy

from src.text import Text, Mode


def levenshtein_distance(file_1: Text, file_2: Text) -> np.array:
    """
    constructs grid which contains number of operations required to transform `file_1` to `file_2`
    """
    grid = np.zeros(shape=(len(file_1) + 1, len(file_2) + 1))
    for row in range(1, len(file_2)+1):
        grid[0, row] = row
    for col in range(1, len(file_1)+1):
        grid[col, 0] = col

    for r in range(1, grid.shape[0]):
        for c in range(1, grid.shape[1]):
            if file_2(c) == file_1(r):
                sub_cost = 0
            else:
                sub_cost = 1

            grid[r, c] = min(grid[r-1, c-1] + sub_cost,  # replace
                             grid[r-1, c] + 1,  # insert
                             grid[r, c-1] + 1)  # delete
    return grid


def get_operations(file_1: Text, file_2: Text):
    """
    using Levenshtein distance, calculates which deletions/insertions need to be made
    marks lines that need to be deleted by setting mode of lines in `file_1` to `Mode.DELETION`
    :return: list of lines from `file_2` which need to be inserted into `file_1`
    """
    insertions = list()

    grid = levenshtein_distance(file_1, file_2)
    # traverse the grid and determine performed operations
    row, col = grid.shape[0] - 1, grid.shape[1] - 1
    current_val = grid[row, col]
    while col >= 0 and row >= 0:
        action = np.argmin([grid[row-1, col-1],  # replace
                            grid[row-1, col],  # insert
                            grid[row, col-1]])  # delete
        if action == 0:
            row, col = row-1, col-1
        elif action == 1:
            row, col = row-1, col
        else:
            row, col = row, col-1

        if grid[row, col] < current_val:
            if action == 1:
                file_1(row+1).set_mode(Mode.DELETION)
            elif action == 2:
                insertions.append(file_2(col+1).set_mode(Mode.INSERTION))
            else:
                file_1(row+1).set_mode(Mode.DELETION)
                insertions.append(file_2(col+1).set_mode(Mode.INSERTION))
            current_val = grid[row, col]

    return sorted(insertions, key=lambda x: x.line_number)
