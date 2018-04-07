#!/usr/bin/env python

import os
import sys
from collections import Counter


def read_extensions(txt_file):
    """return tuple of extensions read from Extensions.txt file from same directory as big txt file"""

    # FIXME we assume Extensions.txt saved in same dir as other, big .txt file
    ext_file = os.path.join(os.path.dirname(txt_file), 'Extensions.txt')

    if not os.path.exists(ext_file):
        raise IOError('cannot find extensions in %s' % ext_file)

    # FIXME fixed format of Extensions.txt file assumed, newline separated extensions
    with open(ext_file) as fh:
        ext_lines = fh.read().splitlines()
    return tuple(ext_lines)


def write_tally_csv_file(fname, exts):
    """write csv file that shows counts of files with specified input extensions"""

    # verify output csv file does not exist yet
    csv_file = fname.replace('.txt', '_tally.csv')
    if os.path.exists(csv_file):
        raise IOError('output CSV file %s exists already' % csv_file)

    # read file into raw lines list
    with open(fname) as f:
        raw_lines = f.read().splitlines()

    # right strip each line
    rstrip_lines = [raw_line.rstrip() for raw_line in raw_lines]

    # keep only lines that end with one of the extensions we specified
    ext_lines = [s for s in rstrip_lines if s.endswith(exts)]

    # reverse matching ext lines and sort (going backwards ftw)
    rev_lines = [s[::-1] for s in ext_lines]
    rev_lines.sort()

    # reverse each line again, so now their frontwards
    lines = [x[::-1] for x in rev_lines]

    # iterate over extensions to count total for each and dupes too
    headers = []
    values = []
    for ext in exts:
        headers += [ext, ext + '_dupes']
        ext_lines = [a for a in lines if a.endswith(ext)]
        c = Counter(ext_lines)
        num_unique = len(c)
        num_total = sum(c.values())
        num_dupes = num_total - num_unique
        values += [num_total, num_dupes]

    with open(csv_file, "w") as text_file:
        text_file.write(','.join(headers))
        text_file.write('\n' + ','.join([str(i) for i in values]))


def main(input_file):
    """"""
    extensions = read_extensions(input_file)
    write_tally_csv_file(input_file, extensions)


if __name__ == '__main__':
    main(sys.argv[1])
