import sys
import os


def check_error_file_path(file_path):
    if not os.path.isfile(file_path):
        show_instructions()
        raise TypeError(f'{file_path} is not a file path or file does not exist!')


def show_instructions():
    print("The command should look like:\n"
          "python3 join.py ./data/Employee.csv ./data/turnover.csv Age\n"
          "OR\n"
          "python3 join.py ./data/Employee.csv ./data/turnover.csv Age inner\n"
          "The last parameter (type of join) is optional.\n")


def parse_arguments() -> tuple:
    join_types = {'inner', 'left', 'right'}
    argv = sys.argv
    argc = len(argv)

    if argc < 4 or argc > 5:
        show_instructions()
        raise TypeError(f'The number of arguments must be 4 or 5 not {argc}.')

    # join.py file_path1 file_path2 column_name join_type
    file_path1 = argv[1]
    file_path2 = argv[2]
    column_name = argv[3]
    if argc == 4:
        # default join_type
        join_type = 'inner'
    else:
        join_type = argv[4]

    check_error_file_path(file_path1)
    check_error_file_path(file_path2)

    if not join_type in join_types:
        show_instructions()
        raise TypeError(f'{join_type} is not available type of join: inner, left, right')

    return file_path1, file_path2, column_name, join_type
