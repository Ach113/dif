import os
import sys
import numpy as np
from enum import Enum
from typing import List, Dict


class Color:
    RED = '\033[31m'
    GREEN = '\033[92m'
    END = '\033[0m'


class Mode(Enum):
    NO_ACTION = 2
    INSERTION = 1
    DELETION = 0

    def __str__(self):
        if self == Mode.DELETION:
            return '-'
        if self == Mode.INSERTION:
            return '+'
        return " "


class Line:

    def __init__(self, line_number: int, content: str, mode: Mode):
        self.line_number = line_number
        self.content = content
        self.mode = mode

    def __str__(self):
        text = self.content.strip('\n')
        return f"{self.line_number} {self.mode} {text}"

    def __eq__(self, other: 'Line'):
        return self.content == other.content

    def set_mode(self, mode: Mode) -> 'Line':
        self.mode = mode
        return self


class Text:

    def __init__(self, file_name: str):
        self.lines = self.read_file(file_name)

    def __call__(self, line_number: int) -> Line:
        """
        returns line contents at a given line number
        """
        return self.lines[line_number]

    def __len__(self) -> int:
        return len(self.lines)

    def display_text(self, inserts: List[Line]):
        """
        displays changes in text in appropriate order and corresponding color
        :param inserts: list of lines from `file_2` that need to be inserted into `file_1`
        """
        if all(x.mode == Mode.NO_ACTION for x in list(self.lines.values())) and len(inserts) == 0:
            return
        line_number, insertion_counter = 1, 0
        for _, line in self.lines.items():

            insertion_counter = 0
            while inserts and inserts[0].line_number <= line_number:
                l = inserts.pop(0)
                text = l.content.strip('\n')
                print(Color.GREEN + f'{line_number} {l.mode} {text}' + Color.END)
                insertion_counter += 1

            line_number += insertion_counter
            text = line.content.strip('\n')
            if line.mode == Mode.DELETION:
                print(Color.RED + f'{line_number-1} {line.mode} {text}' + Color.END)
            else:
                print(f'{line_number} {line.mode} {text}')
                line_number += 1

    @staticmethod
    def read_file(file_name: str) -> Dict:
        if not os.path.exists(file_name):
            raise Exception(f"error: file `{file_name}` not found")
        line_dict = {}
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                line_object = Line(i+1, line, Mode.NO_ACTION)
                line_dict[i+1] = line_object
        return line_dict


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


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: dif <file1> <file2>")
        sys.exit(-1)

    file_1 = Text(file_name=sys.argv[1])
    file_2 = Text(file_name=sys.argv[2])

    file_1.display_text(get_operations(file_1, file_2))
