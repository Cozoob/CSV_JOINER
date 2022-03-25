from __future__ import with_statement

import sys
import os


def check_error_file_path(file_path: str):
    """
        Checks if the file path is correct
        or if the file even exists.

        :param file_path: The path of the CSV file.
        :type file_path: str
    """
    if not os.path.isfile(file_path):
        show_instructions()
        raise TypeError(f'{file_path} is not a file path or file does not exist!')


def show_instructions():
    """
        Prints helpful message (how to use program).
    """
    print("The command should look like:\n"
          "python3 join.py ./data/Employee.csv ./data/MFG10YearTerminationData.csv Age\n"
          "OR\n"
          "python3 join.py ./data/Employee.csv ./data/MFG10YearTerminationData.csv Age inner\n"
          "The last parameter (type of join) is optional.\n")


def parse_arguments() -> tuple:
    """
    Checks arguments from the user.

    :return: The tuple that contains two file paths,
    column name and type of join.
    :rtype: tuple
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

    if join_type not in join_types:
        show_instructions()
        raise TypeError(f'{join_type} is not available type of join: inner, left, right')

    return file_path1, file_path2, column_name, join_type


def find_index_of_column(header: str, column_name: str) -> int:
    """
        Finds the index of the column with the given name.

        :param header: The header line of the CSV file.
        :param column_name: The name of the column to find its index.
        :type header: str
        :type column_name: str
        :return: The index of the column.
        :rtype: int
    """
    arr = header.split(',')
    try:
        idx = arr.index(column_name)
    except ValueError:
        raise ValueError(f'The name {column_name} does not exist in one of the files!')

    return idx


def parse_data_line(line1: str, line2: str, column_index1: int, column_index2: int):
    """
        Joins and prints the two lines from CSV files.

        :param line1: The first line to join.
        :param line2: The second line to join.
        :param column_index1: The index of the joining column in the first line.
        :param column_index2: The index of the joining column in the second line.
        :type line1: str
        :type line2: str
        :type column_index1: int
        :type column_index2: int
    """
    new_line = str(line1)
    new_line = new_line.rstrip()
    new_line = new_line.split(',')

    new_line2 = str(line2)
    new_line2 = new_line2.rstrip()
    new_line2 = new_line2.split(',')

    if column_index2 != -1:
        new_line2.remove(new_line2[column_index2])
    else:
        new_line.remove(new_line[column_index1])

    new_line.extend(new_line2)

    line_to_print = ''
    for _ in range(len(new_line)):
        line_to_print += '{: >13} '

    print(line_to_print.format(*new_line))


def split_and_strip(line: str) -> [str]:
    """
        Copies the string, deletes the \n sign and
        splits by comma.

        :param line: The line to split and rstrip.
        :type line: str
        :return: The array of strings.
        :rtype: [str]
   """
    new_line = str(line)
    new_line = new_line.rstrip()
    return new_line.split(',')


def print_non_inner_join(file, header: str, taken_rows: set, join_type: str, column_index: int):
    """
        Prints non-inner type of join in order to "fill" NULL values.

        :param file: The handle of the file.
        :param header: The header of the second file to get the
        number of the NULLs.
        :param taken_rows: The set of already printed rows of the file.
        :param join_type: The type of the join.
        :param column_index: The column_index to pass it
        to the parse_data_line function.
        :type file: TextIO
        :type header: str
        :type taken_rows: set
        :type join_type: str
        :type column_index: int
    """
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
            line = file.readline()
            counter += 1
            continue

        if join_type == 'left':
            parse_data_line(line, filler, -1, column_index)

        if join_type == 'right':
            parse_data_line(filler, line, column_index, -1)

        line = file.readline()
        counter += 1


def join_files(file_path1: str, file_path2: str, column_name: str, join_type: str):
    """
        The actual main algorithm for printing the joined files.

        :param file_path1: The path of the first file.
        :param file_path2: The path of the second file.
        :param column_name: The name of the column to join on.
        :param join_type: The type of the join.
        :type file_path1: str
        :type file_path2: str
        :type column_name: str
        :type join_type: str
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

            if join_type == 'right':
                parse_data_line(header1, header2, column_index1, -1)
            else:
                parse_data_line(header1, header2, -1, column_index2)

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
                        parse_data_line(line1, line2, -1, column_index2)

                    i2 += 1
                    line2 = file2.readline()

                i1 += 1
                line1 = file1.readline()

            if join_type == 'left':
                print_non_inner_join(file1, header2, taken_rows2, join_type, column_index2)

            if join_type == 'right':
                print_non_inner_join(file2, header1, taken_rows1, join_type, column_index1)

    except EnvironmentError:
        raise EnvironmentError('EnvironmentError occurred!')
