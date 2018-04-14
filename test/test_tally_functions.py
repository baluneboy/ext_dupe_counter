import os
import unittest
from tally import read_extensions, write_tally_csv_file
from shutil import copyfile


class TestTallyFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ avoid calling setUp for each test, so use setUpClass()
            and store the result as class variable
        """
        super(TestTallyFunctions, cls).setUpClass()

        # if tally csv file exists in okay subdir, then delete it
        cls.ok_tally_file = './test/okay/biglist_tally.csv'
        if os.path.exists(cls.ok_tally_file):
            os.remove(cls.ok_tally_file)

        # make sure Extensions.txt exists on user desktop
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        # FIXME only run tests on dev machines, so we do not clobber actual user files
        if not desktop_dir.startswith('/Users/ken'):
            raise SystemExit

        cls.ext_file = os.path.join(desktop_dir, 'Extensions.txt')
        if not os.path.exists(cls.ext_file):
            copyfile('./test/okay/Extensions.txt', cls.ext_file)

    def test_read_extensions(self):
        exts_expected = ('abc', 'def', 'ghi')
        exts_from_file = read_extensions(self.ext_file)
        self.assertEqual(exts_expected, exts_from_file)

    def test_read_extensions_missing_file(self):
        with self.assertRaises(IOError) as ecm:
            read_extensions('./missing_extensions_file/Extensions.txt')
        exception = ecm.exception
        self.assertEqual(exception.args, ('cannot find extensions in ./missing_extensions_file/Extensions.txt', ))

    def test_write_csv_tally_file(self):
        exts_expected = ('abc', 'def', 'ghi')
        input_file = './test/okay/biglist.txt'
        exts_from_file = read_extensions(self.ext_file)
        self.assertEqual(exts_expected, exts_from_file)
        write_tally_csv_file(input_file, exts_from_file)

    def test_write_file_already_exists(self):
        exts_expected = ('abc', 'def', 'ghi')
        input_file = './test/tally_file_already_exists/biglist.txt'
        exts_from_file = read_extensions(self.ext_file)
        self.assertEqual(exts_expected, exts_from_file)
        with self.assertRaises(IOError) as ecm:
            write_tally_csv_file(input_file, exts_from_file)
        exception = ecm.exception
        self.assertEqual(exception.args,
                         ('output CSV file ./test/tally_file_already_exists/biglist_tally.csv '
                          'exists already',))

    @classmethod
    def tearDownClass(cls):
        """ use this to avoid calling tearDown for each test """
        super(TestTallyFunctions, cls).tearDownClass()

        # if tally csv file exists in okay subdir, then delete it
        if os.path.exists(cls.ok_tally_file):
            os.remove(cls.ok_tally_file)

        # make sure Extensions.txt exists on user desktop
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        cls.ext_file = os.path.join(desktop_dir, 'Extensions.txt')
        if not os.path.exists(cls.ext_file):
            copyfile('./test/okay/Extensions.txt', cls.ext_file)


if __name__ == '__main__':
    unittest.main()
