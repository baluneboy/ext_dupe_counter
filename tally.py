#!/usr/bin/env python

import os
import sys
import hashlib
import datetime
from collections import Counter
from confiparser_tally import COLUMNS, read_config


# TODO no more drag-n-drop, instead use recursive file listing
# TODO derive filename for run list OR just use RunList_DATETIMESTAMP.txt
# TODO config file for which columns to show in run list & output directory

# TODO ask Mark what columns are of interest file size, date modified, md5sum, name
# TODO ask Mark what is a duplicate because on local machine, 2 files cannot share name


def get_md5(fname, block_size=2**20):
    m = hashlib.md5()
    with open(fname, "rb") as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def get_fsize(fname):
    return os.stat(fname).st_size


def get_fdate(fname):
    return datetime.datetime.fromtimestamp(os.path.getmtime(fname))


def get_matching_file_extensions(top_dir, exts):
    """return list of filenames matching extensions via recursive directory walk"""
    kept_filenames = []
    for root, dirs, files in os.walk(top_dir):
        kept_filenames += [os.path.join(root, s) for s in files if s.endswith(exts)]
    return kept_filenames


def get_files_info(top_dir, exts, cols):
    files = get_matching_file_extensions(top_dir, exts)
    files_info = []
    for f in files:
        file_info = (f, )
        if cols['md5']:
            file_info += (get_md5(f), )
        if cols['date']:
            file_info += (get_fdate(f), )
        if cols['size']:
            file_info += (get_fsize(f), )
        files_info += file_info
        # print get_md5(f), \
        #     get_fdate(f).strftime('%Y-%m-%d %H:%M:%S'), \
        #     "{:>15,}".format(get_fsize(f)), \
        #     f
    return files_info


class MyIOError(IOError):
    def __init__(self, *args, **kwargs):
        IOError.__init__(self, *args, **kwargs)


def read_extensions(config_file):
    """return tuple of extensions read from input file [e.g. ~/Desktop/Extensions.txt]"""

    if not os.path.exists(config_file):
        raise IOError('cannot find extensions in %s' % config_file)

    # FIXME fixed format of Extensions.txt file assumed, newline separated extensions
    with open(config_file) as fh:
        ext_lines = fh.read().splitlines()

    print '%d extensions found in Extensions.txt file' % len(ext_lines)

    return tuple(ext_lines)


def write_tally_csv_file(files_info):
    """write csv file that shows counts of files with specified input extensions"""

    print files_info
    raise SystemExit

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
    with open(csv_file, "w") as tconfig_file:
        tconfig_file.write(','.join(headers))
        tconfig_file.write('\n' + ','.join([str(i) for i in values]) + '\n')


def main():
    """tally lines (and dupes) associated with specified extensions
    - use extensions to process the input file(s)
    - write results to csv output file; same name as input but extension changed
    """

    # get/verify first argument as top directory to walk
    top_dir = sys.argv[1]
    if not os.path.isdir(top_dir):
        raise IOError('first and only argument "%s" is not a directory' % top_dir)

    # read config_file
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    config_file = os.path.join(desktop_dir, 'tally_config.txt')
    config = read_config(cfg_fname=config_file)

    # output directory
    output_dir = config.get('RunListDestination', 'output_dir')
    if output_dir.lower() == 'here':
        output_dir = top_dir

    # csv filename; short-circuit if _tally.csv file already exists at destination
    csv_fname = os.path.join(output_dir, os.path.basename(output_dir) + '_tally.csv')
    if os.path.exists(csv_fname):
        raise MyIOError('aborted because output CSV file %s exists already' % csv_fname)

    # get configuration info
    exts = config.get('RunListExtensions', 'extensions')
    extensions = tuple([x.lstrip().rstrip() for x in exts.split(',')])
    print 'extensions:', extensions

    columns = {}
    for k in COLUMNS:
        columns[k] = config.getboolean('RunListColumns', k)
    print 'columns:', columns

    # get each extension-matching files' info
    files_info = get_files_info(top_dir, extensions, columns)

    # write tally CSV file
    write_tally_csv_file(files_info)


if __name__ == '__main__':
    main()
