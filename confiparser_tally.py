#!/usr/bin/env python

import os
import ConfigParser


COLUMNS = ['md5', 'date', 'size', 'dupes']


def get_default_config_fname():
    """return string with default config filename"""
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    return os.path.join(desktop_dir, 'tally_config.txt')


def write_config(cfg_fname=None):
    """write default config to file specified"""

    if cfg_fname is None:
        cfg_fname = get_default_config_fname()

    if os.path.exists(cfg_fname):
        raise IOError('config file: %s EXISTS ALREADY' % cfg_fname)

    config = ConfigParser.SafeConfigParser()

    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.

    config.add_section('RunListDestination')
    config.set('RunListDestination', 'output_dir', 'here')

    config.add_section('RunListExtensions')
    config.set('RunListExtensions', 'extensions', 'tiff, next, ccu, mei, log, txt, metadata')

    config.add_section('RunListColumns')
    for key in COLUMNS:
        config.set('RunListColumns', key,  'True')
    config.set('RunListColumns', 'dupes', 'False')

    # Writing our configuration file to 'tally.cfg'
    with open(cfg_fname, 'wb') as configfile:
        config.write(configfile)


def read_config(cfg_fname=None):
    """do something"""

    if cfg_fname is None:
        cfg_fname = get_default_config_fname()

    config = ConfigParser.SafeConfigParser()

    if not os.path.exists(cfg_fname):
        print 'creating %s because it did not exist' % cfg_fname
        write_config(cfg_fname)

    print 'reading %s' % cfg_fname
    config.read(cfg_fname)

    return config


def main():
    demo_read()


if __name__ == '__main__':
    main()
