import sys
import os
import unittest
import tempfile

from csvjoin import functions
from io import StringIO


class Capturing(list):
    """
    Captures the output from the print() function.

    Only for tests.
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


class MyTestCase(unittest.TestCase):

    def test_parse_arguments_number_of_arguments(self):
        # Too few arguments
        sys.argv = ['join.py']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        # Too many arguments
        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv', 'Age', 'left', 'left']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv', 'Age', 'left', 'left',
                    '../data/turnover.csv', 'Age', 'left', 'left']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

    def test_parse_arguments_type_of_join(self):
        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv', 'Age', 'leftt']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv', 'Age', 'rigt']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/MFG10YearTerminationData.csv', 'Age', 'down']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

    def test_check_error_file_path(self):
        with self.assertRaises(TypeError):
            functions.check_error_file_path('./data/Employee.csv')

        with self.assertRaises(TypeError):
            functions.check_error_file_path('Employee.csv')

        with self.assertRaises(TypeError):
            functions.check_error_file_path(0)

    def test_check_find_index_of_column(self):
        header = 'EmployeeID,RecordID,Gender'

        with self.assertRaises(ValueError):
            functions.find_index_of_column(header, 'Employeeid')

        with self.assertRaises(ValueError):
            functions.find_index_of_column(header, 'a')

        with self.assertRaises(ValueError):
            functions.find_index_of_column(header, 'gender')

    def test_join(self):

        # test inner join
        tmp1 = tempfile.NamedTemporaryFile(delete=False)
        tmp2 = tempfile.NamedTemporaryFile(delete=False)

        tmp1.write(b'Age,Gender,ID\n'
                   b'7,Male,1\n'
                   b'8,Female,2\n'
                   b'3,Female,3')

        tmp2.write(b'Age,Gender,ID\n'
                   b'7,Male,1\n'
                   b'8,Female,2\n'
                   b'3,Female,3')

        tmp1.close()
        tmp2.close()

        results = [['Age', 'Gender', 'ID', 'Age', 'Gender'],
                   ['7', 'Male', '1', '7', 'Male'],
                   ['8', 'Female', '2', '8', 'Female'],
                   ['3', 'Female', '3', '3', 'Female']]

        with Capturing() as output:
            functions.join_files(tmp1.name, tmp2.name, 'ID', 'inner')

        for i in range(len(output)):
            output[i] = output[i].split()

        self.assertEqual(results, output)

        tmp3 = tempfile.NamedTemporaryFile(delete=False)

        tmp3.write(b'Age,Gender,ID\n'
                   b'7,Male,1\n'
                   b'8,Female,2\n')

        tmp3.close()

        results1 = results[:len(results) - 1]

        with Capturing() as output:
            functions.join_files(tmp1.name, tmp3.name, 'ID', 'inner')

        for i in range(len(output)):
            output[i] = output[i].split()

        self.assertEqual(results1, output)

        # test left join
        tmp4 = tempfile.NamedTemporaryFile(delete=False)

        tmp4.write(b'Age,Gender,ID\n'
                   b'7,Male,1\n'
                   b'8,Female,20\n')

        tmp4.close()

        results3 = [['Age', 'Gender', 'ID', 'Age', 'Gender'],
                    ['7', 'Male', '1', '7', 'Male'],
                    ['8', 'Female', '2', 'NULL', 'NULL'],
                    ['3', 'Female', '3', 'NULL', 'NULL']]

        with Capturing() as output:
            functions.join_files(tmp1.name, tmp4.name, 'ID', 'left')

        for i in range(len(output)):
            output[i] = output[i].split()

        self.assertEqual(results3, output)

        # test right join
        results4 = [['Age', 'Gender', 'Age', 'Gender', 'ID'],
                    ['7', 'Male', '7', 'Male', '1'],
                    ['NULL', 'NULL', '8', 'Female', '20']]

        with Capturing() as output:
            functions.join_files(tmp1.name, tmp4.name, 'ID', 'right')

        for i in range(len(output)):
            output[i] = output[i].split()

        self.assertEqual(results4, output)

        # test empty result of inner join
        tmp5 = tempfile.NamedTemporaryFile(delete=False)

        tmp5.write(b'Age,Gender,ID\n'
                   b'7,Male,10\n'
                   b'8,Female,20\n')

        tmp5.close()

        results5 = [['Age', 'Gender', 'ID', 'Age', 'Gender']]

        with Capturing() as output:
            functions.join_files(tmp1.name, tmp5.name, 'ID', 'inner')

        for i in range(len(output)):
            output[i] = output[i].split()

        self.assertEqual(results5, output)

        # delete tmp files
        os.remove(tmp1.name)
        os.remove(tmp2.name)
        os.remove(tmp3.name)
        os.remove(tmp4.name)
        os.remove(tmp5.name)


if __name__ == '__main__':
    unittest.main()
