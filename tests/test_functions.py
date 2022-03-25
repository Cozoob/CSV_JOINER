import unittest
from csvjoin import functions
import sys

class MyTestCase(unittest.TestCase):

    def test_parse_arguments_number_of_arguments(self):
        # Too few arguments
        sys.argv = ['join.py']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        # Too many arguments
        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv', 'Age', 'left', 'left']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv', 'Age', 'left', 'left',
                    '../data/turnover.csv', 'Age', 'left', 'left']
        with self.assertRaises(TypeError):
            functions.parse_arguments()


    def test_parse_arguments_type_of_join(self):

        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv', 'Age', 'leftt']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv', 'Age', 'rigt']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

        sys.argv = ['join.py', '../data/Employee.csv', '../data/turnover.csv', 'Age', 'down']
        with self.assertRaises(TypeError):
            functions.parse_arguments()

    def test_check_error_file_path(self):

        with self.assertRaises(TypeError):
            functions.check_error_file_path('./data/Employee.csv')

        with self.assertRaises(TypeError):
            functions.check_error_file_path('Employee.csv')

        with self.assertRaises(TypeError):
            functions.check_error_file_path(0)


if __name__ == '__main__':
    unittest.main()
