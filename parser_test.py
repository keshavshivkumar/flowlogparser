import unittest
import os
from parser import log_parser

class TestParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestParser, self).__init__(*args, **kwargs)
        self.files_to_cleanup = []

    def assert_files(self, path1, path2):
        '''Assert the files/file paths are provided'''
        if not (path1 and path2):
            raise AssertionError('File needs to be provided!')
    
    def test_filenames_provided(self):
        '''Test that the filenames are provided.'''
        with self.assertRaises(AssertionError):
            self.assert_files('', 'lookup.csv')
        with self.assertRaises(AssertionError):
            self.assert_files('sampleinput.csv', '')
        try:
            self.assert_files('sampleinput.csv', 'lookup.csv')
        except AssertionError:
            self.fail('Unexpected Error!')
    
    def test_valid_files(self):
        '''Test that log_parser can handle valid files'''
        try:
            log_parser('sampleinput.csv', 'samplelookuptable.csv', 'output.csv')
        except FileNotFoundError as e:
            self.fail(f"log_parser raised FileNotFoundError unexpectedly: {e}")
        except Exception as e:
            self.fail(f"log_parser raised an unexpected exception: {e}")
        finally:
            self.files_to_cleanup.append('output.csv')

    def test_nonexistent_files(self):
        '''Test how log_parser handles non-existent files'''
        with self.assertRaises(SystemExit):
            log_parser('nonexistent_input.csv', 'samplelookuptable.csv', 'output.csv')
        
        with self.assertRaises(SystemExit):
            log_parser('sampleinput.csv', 'nonexistent_lookup.csv', 'output.csv')
    
    def test_empty_files(self):
        '''Test how log_parser handles empty files'''
        empty_input = 'empty_input.csv'
        empty_lookup = 'empty_lookup.csv'
        output_file = 'output.csv'
        with open('empty_input.csv', 'w') as f1, open('empty_lookup.csv', 'w') as f2:
            pass

        with self.assertRaises(SystemExit) as cm:
            log_parser('empty_input.csv', 'empty_lookup.csv', 'output.csv')

        self.assertEqual(cm.exception.code, 1)
        self.files_to_cleanup.extend([empty_input, empty_lookup, output_file])

    def tearDown(self):
        '''Remove generated test files after each test'''
        for filename in self.files_to_cleanup:
            try:
                os.remove(filename)
            except OSError as e:
                print(f"Error: {filename} : {e.strerror}")
if __name__ == '__main__':
    unittest.main()