#!/usr/bin/env python

import os
import sys
from collections import Counter


def read_extensions(txt_file):
    """return tuple of extensions read from Extensions.txt file in same directory as big txt file"""
    ext_file = os.path.join(os.path.dirname(txt_file), 'Extensions.txt')
    if not os.path.exists(ext_file):
        print 'abort: cannot find extensions in %s' % ext_file
        return None

    with open(ext_file) as fh:
        ext_lines = fh.read().splitlines()
    return tuple(ext_lines)


def write_csv_tally_file(fname, exts):
    """write csv file that shows counts of files with specified input extensions"""

    # verify output csv file does not exist yet
    csv_file = fname.replace('.txt', '_tally.csv')
    if os.path.exists(csv_file):
        print 'abort: output CSV file %s exists already' % csv_file
        return -1

    # read file into raw lines list
    with open(fname) as f:
        raw_lines = f.read().splitlines()

    # right strip each line
    rstrip_lines = [raw_line.rstrip() for raw_line in raw_lines]
    old_lines = [s for s in rstrip_lines if s.endswith(exts)]

    # reverse matching ext lines and sort (backwards strings ftw)
    rev_lines = [s[::-1] for s in old_lines]
    rev_lines.sort()

    # reverse each line now to frontwards
    lines = [x[::-1] for x in rev_lines]

    # iterate over extensions and count (with count of dupes too)
    hdr_str = ''
    val_str = ''
    for ext in exts:
        hdr_str += '%s,%s,' % (ext, ext + "_dupes")
        ext_lines = [a for a in lines if a.endswith(ext)]
        c = Counter(ext_lines)
        num_unique = len(c)
        num_total = sum(c.values())
        num_dupes = num_total - num_unique
        val_str += '%d,%d,' % (num_total, num_dupes)  # , num_unique

    # print hdr_str.rstrip(',')
    # print val_str.rstrip(',')

    with open(csv_file, "w") as text_file:
        text_file.write(hdr_str.rstrip(','))
        text_file.write('\n' + val_str.rstrip(','))

    return 0


def main(input_file):
    """"""
    extensions = read_extensions(input_file)
    write_csv_tally_file(input_file, extensions)


if __name__ == '__main__':
    main(sys.argv[1])
