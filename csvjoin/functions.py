from __future__ import with_statement

import sys
import os


def check_error_file_path(file_path: str):
    if not os.path.isfile(file_path):
        show_instructions()
        raise TypeError(f'{file_path} is not a file path or file does not exist!')


def show_instructions():
    print("The command should look like:\n"
          "python3 join.py ./data/Employee.csv ./data/MFG10YearTerminationData.csv Age\n"
          "OR\n"
          "python3 join.py ./data/Employee.csv ./data/MFG10YearTerminationData.csv Age inner\n"
          "The last parameter (type of join) is optional.\n")


def parse_arguments() -> tuple:
    """
    Helpful function to check arguments from the user.
    """
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


def find_index_of_column(header: str, column_name: str) -> int:

    arr = header.split(',')
    try:
        idx = arr.index(column_name)
    except ValueError:
        raise ValueError(f'The name {column_name} does not exist in one of the files!')

    return idx

def parse_data_line(line1: str, line2: str, column_index1: int, column_index2: int):

    if column_index1 == -1 or column_index2 == -1:
        print("oppps")
        #TODO DELETE
        pass

    new_line = str(line1)
    new_line = new_line.rstrip()
    new_line = new_line.split(',')

    new_line2 = str(line2)
    new_line2 = new_line2.rstrip()
    new_line2 = new_line2.split(',')
    new_line2.remove(new_line2[column_index2])

    # new_line += tmp[:column_index2-1] + str(line2[column_index2+1:])
    new_line.extend(new_line2)

    line_to_print = ''
    for _ in range(len(new_line)):
        line_to_print += '{: >13} '

    print(line_to_print.format(*new_line))


def split_and_strip(line: str) -> [str]:
    new_line = str(line)
    new_line = new_line.rstrip()
    return new_line.split(',')

def print_non_inner_join(file, header: str, taken_rows: set, join_type: str, column_index1: int, column_index2: int):
    file.seek(0, 0)
    file.readline()
    line = file.readline()

    # creating NULL line string
    header = header.split(',')
    n = len(header)
    filler = ''
    for _ in range(n - 1):
        filler += 'NULL'
        filler += ','
    filler += 'NULL'

    counter = 1
    while line != '':
        if counter in taken_rows:
            # print(taken_rows1)
            # print(taken_rows2)
            # exit(1)
            line = file.readline()
            counter += 1
            continue

        if join_type == 'left':
            parse_data_line(line, filler, column_index1, column_index2)

        if join_type == 'right':
            parse_data_line(filler, line, column_index1, column_index2)

        line = file.readline()
        counter += 1




def join_files(file_path1: str, file_path2: str, column_name: str, join_type: str):
    """
    The actual main algorithm for printing the joined files.
    """
    try:
        # Even though I can have left or right join
        # firstly I need to do inner and after that
        # I can do the rest if needed
        with open(file_path1) as file1, open(file_path2) as file2:
            header1 = str(file1.readline())
            header2 = str(file2.readline())

            # look for the index where column_name appears in header of the CSV files
            column_index1 = find_index_of_column(header1, column_name)
            column_index2 = find_index_of_column(header2, column_name)

            parse_data_line(header1, header2, column_index1, column_index2)

            taken_rows1 = set()
            taken_rows2 = set()

            i1 = 1
            line1 = file1.readline()
            while line1 != '':

                # return to the begging of the file2
                file2.seek(0, 0)
                i2 = 0
                line2 = file2.readline()

                while line2 != '':
                    if i2 == 0:
                        i2 += 1
                        line2 = file2.readline()
                        continue

                    arr1 = split_and_strip(line1)
                    arr2 = split_and_strip(line2)

                    if arr1[column_index1] == arr2[column_index2]:
                        taken_rows1.add(i1)
                        taken_rows2.add(i2)
                        parse_data_line(line1, line2, column_index1, column_index2)

                    i2 += 1
                    line2 = file2.readline()

                i1 += 1
                line1 = file1.readline()

            if join_type == 'left':
                print_non_inner_join(file1, header2, taken_rows2, join_type, column_index1, column_index2)

            if join_type == 'right':
                print_non_inner_join(file2, header1, taken_rows1, join_type, column_index1, column_index2)


    except EnvironmentError:
        print("oooops")