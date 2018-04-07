import os
import unittest
from tally import read_extensions, write_tally_csv_file


class TestTallyFunctions(unittest.TestCase):

    def setUp(self):
        # if tally csv file exists in okay subdir, then delete it
        self.ok_tally_file = './test/okay/biglist_tally.csv'
        if os.path.exists(self.ok_tally_file):
            os.remove(self.ok_tally_file)

    def test_read_extensions(self):
        exts_expected = ('abc', 'def', 'ghi')
        exts_from_file = read_extensions('./test/okay/biglist.txt')
        self.assertEqual(exts_expected, exts_from_file)

    def test_read_extensions_missing_file(self):
        with self.assertRaises(IOError) as ecm:
            read_extensions('./missing_extensions_file/biglist.txt')
        exception = ecm.exception
        self.assertEqual(exception.args, ('cannot find extensions in ./missing_extensions_file/Extensions.txt', ))

    def test_write_csv_tally_file(self):
        exts_expected = ('abc', 'def', 'ghi')
        input_file = './test/okay/biglist.txt'
        exts_from_file = read_extensions(input_file)
        self.assertEqual(exts_expected, exts_from_file)
        write_tally_csv_file(input_file, exts_from_file)

    def test_write_file_already_exists(self):
        exts_expected = ('abc', 'def', 'ghi')
        input_file = './test/tally_file_already_exists/biglist.txt'
        exts_from_file = read_extensions(input_file)
        self.assertEqual(exts_expected, exts_from_file)
        with self.assertRaises(IOError) as ecm:
            write_tally_csv_file(input_file, exts_from_file)
        exception = ecm.exception
        self.assertEqual(exception.args,
                         ('output CSV file ./test/tally_file_already_exists/biglist_tally.csv '
                          'exists already',))


if __name__ == '__main__':
    unittest.main()
