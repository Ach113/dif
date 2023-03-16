import os
from enum import Enum
from typing import List, Dict


class Color:
    RED = '\033[31m'
    GREEN = '\033[92m'
    END = '\033[0m'


class Mode(Enum):
    DELETION = 0
    INSERTION = 1
    NO_ACTION = 2

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