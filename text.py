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

    def __lt__(self, other):
        return self.value < other.value

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
        stack = list()
        for _, line in self.lines.items():
            insertion_counter = 0
            if inserts and inserts[0].line_number <= line_number:
                l = inserts.pop(0)
                l.line_number = line_number
                stack.append(l)
                insertion_counter += 1

            line_number += insertion_counter

            if line.mode == Mode.DELETION:
                line.line_number = line_number - 1
                stack.append(line)
            else:
                line.line_number = line_number
                stack.append(line)
                line_number += 1
        # sort wrt line number, mode (deletions first, then insertions, finally default)
        stack = sorted(stack, key=lambda x: (x.line_number, x.mode))
        # rearrange deletions
        # i = 0
        # prev_del_idx = -1
        # prev_swap_idx = -1
        # while i < len(stack):
        #     if stack[i].mode == Mode.DELETION and prev_del_idx > 0 and \
        #             stack[i].line_number - stack[prev_del_idx].line_number == 1:
        #         prev_del_idx = i
        #         prev_swap_idx = max(i+1, prev_swap_idx)
        #         while stack[prev_swap_idx].mode != Mode.DELETION:
        #             prev_swap_idx += 1
        #         prev_swap_idx += 1
        #         stack[i], stack[prev_swap_idx] = stack[prev_swap_idx], stack[i]
        #     else:
        #         prev_del_idx = i
        #     i += 1

        self.display(stack)

    @staticmethod
    def display(stack: list):

        for line in stack:
            text = line.content.strip('\n')
            if line.mode == Mode.DELETION:
                print(Color.RED + f'{line.line_number} - {text}' + Color.END)
            elif line.mode == Mode.INSERTION:
                print(Color.GREEN + f'{line.line_number} + {text}' + Color.END)
            else:
                print(f'{line.line_number}   {text}')

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
