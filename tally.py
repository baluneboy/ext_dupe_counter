#!/usr/bin/env python

import os
import sys
import fnmatch
from glob import glob
from collections import Counter


# TODO no more drag-n-drop, instead use recursive file listing
# TODO derive filename for run list


def demo_walk(top_dir, exts):
    """return list of filenames matching extensions via recursive directory walk"""
    kept_filenames = []
    for root, dirs, files in os.walk(top_dir):
        kept_filenames += [os.path.join(root, s) for s in files if s.endswith(exts)]
    return kept_filenames


top_dir = '/Users/ken/Projects/PyCharm/ext_dupe_counter/test'
exts = ('txt', 'tiff')
keepers = demo_walk(top_dir, exts)
for k in keepers:
    print k
raise SystemExit


class MyIOError(IOError):
    def __init__(self,*args,**kwargs):
        IOError.__init__(self, *args, **kwargs)


def read_extensions(ext_file):
    """return tuple of extensions read from input file [e.g. ~/Desktop/Extensions.txt]"""

    if not os.path.exists(ext_file):
        raise IOError('cannot find extensions in %s' % ext_file)

    # FIXME fixed format of Extensions.txt file assumed, newline separated extensions
    with open(ext_file) as fh:
        ext_lines = fh.read().splitlines()

    print '%d extensions found in Extensions.txt file' % len(ext_lines)

    return tuple(ext_lines)


def write_tally_csv_file(fname, exts):
    """write csv file that shows counts of files with specified input extensions"""

    # verify output csv file does not exist yet
    csv_file = fname.replace('.txt', '_tally.csv')
    if os.path.exists(csv_file):
        raise MyIOError('output CSV file %s exists already' % csv_file)

    # read file into raw lines list
    with open(fname) as f:
        raw_lines = f.read().splitlines()
    print '%d lines read from %s' % (len(raw_lines), fname)

    # right strip each line
    rstrip_lines = [raw_line.rstrip() for raw_line in raw_lines]

    # keep only lines that end with one of the extensions we specified
    kept_lines = [s for s in rstrip_lines if s.endswith(exts)]

    # iterate over extensions to count total for each and dupes too
    headers = []
    values = []
    for ext in exts:
        headers += [ext, ext + '_dupes']
        ext_lines = [a for a in kept_lines if a.endswith(ext)]
        c = Counter(ext_lines)
        num_unique = len(c)  # unique lines for this ext
        num_total = sum(c.values())  # total count for this ext
        num_dupes = num_total - num_unique  # dupe count for this ext
        values += [num_total, num_dupes]

    # write results to output csv file
    with open(csv_file, "w") as text_file:
        text_file.write(','.join(headers))
        text_file.write('\n' + ','.join([str(i) for i in values]) + '\n')


def main():
    """tally lines (and dupes) associated with specified extensions
    - use extensions to process the input file(s)
    - write results to csv output file; same name as input but extension changed
    """
    # read extensions from Desktop that has Extensions.txt file
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    ext_file = os.path.join(desktop_dir, 'Extensions.txt')
    extensions = read_extensions(ext_file)

    # iterate over files specified on command line
    for txt_file in sys.argv[1:]:
        try:
            write_tally_csv_file(txt_file, extensions)
        except MyIOError:
            print 'did not process %s because its "*_tally.csv" file already exists' % txt_file
        except Exception:
            print 'could not process %s (not sure what happened)' % txt_file


if __name__ == '__main__':
    main()
