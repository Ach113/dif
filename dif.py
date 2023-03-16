import sys

from src.text import Text
from src.util import get_operations


def main():
    if len(sys.argv) != 3:
        print("usage: dif <file1> <file2>")
        sys.exit(-1)

    file_1 = Text(file_name=sys.argv[1])
    file_2 = Text(file_name=sys.argv[2])

    file_1.display_text(get_operations(file_1, file_2))


if __name__ == '__main__':
    main()
