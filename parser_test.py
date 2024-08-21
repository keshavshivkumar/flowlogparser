import unittest
import os
from parser import log_parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test_input.csv'
        self.lookup_file = 'test_lookup.csv'
        self.output_file = 'test_output.csv'

        with open(self.input_file, 'w') as f:
            f.write("1,2,3,4,5,6,7,8,9,10,11,12,13,14\n")
            f.write("1,2,3,4,5,6,7,8,9,10,80,12,13,6\n") 

        with open(self.lookup_file, 'w') as f:
            f.write("80,6,Tag1\n")

        self.files_to_cleanup = [self.input_file, self.lookup_file, self.output_file]

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

    def test_tag_counts(self):
        '''Test that the code correctly tracks the counts of the tags'''
        log_parser(self.input_file, self.lookup_file, self.output_file)
        with open(self.output_file, 'r') as f:
            output = f.read()

        self.assertIn('tag1,1\n', output)

    def test_port_protocol_counts(self):
        '''Test that the code correctly tracks the counts of the port-protocol pairs'''
        log_parser(self.input_file, self.lookup_file, self.output_file)
        with open(self.output_file, 'r') as f:
            output = f.read()

        self.assertIn('80,tcp,1\n', output)

    def test_no_matching_tag(self):
        '''Test that the code correctly tracks the counts of the untagged'''
        with open(self.lookup_file, 'a') as f:
            f.write("90,6,Tag1\n")  # adding a new tag that does not match in log file
        log_parser(self.input_file, self.lookup_file, self.output_file)
        with open(self.output_file, 'r') as f:
            output = f.read()

        self.assertIn('Untagged,1\n', output)

    def tearDown(self):
        '''Remove generated test files after each test'''
        for filename in self.files_to_cleanup:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except OSError as e:
                    print(f"Error: {filename} : {e.strerror}")

if __name__ == '__main__':
    unittest.main()