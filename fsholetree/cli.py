# Tool to generate file tree with empty files based on real file tree.
# Copyright (C) 2019  Ivan Mironov <mironov.ivan@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import logging
import sys

import fsholetree.holetree as holetree


_LOG = logging.getLogger()


def _setup_logging(log_level):
    _LOG.setLevel({
        'N': logging.NOTSET,
        'D': logging.DEBUG,
        'I': logging.INFO,
        'W': logging.WARNING,
        'E': logging.ERROR,
        'C': logging.CRITICAL,
    }[log_level[0]])

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname).1s] %(message)s')
    handler.setFormatter(formatter)

    _LOG.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(
        'fsholetree',
        description='Tool to generate file tree with empty files based on '
                    'real file tree',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'SOURCE',
        help='Path to source directory tree')
    parser.add_argument(
        'DESTINATION',
        help='Path to resulting SquashFS image file')
    parser.add_argument(
        '-T',
        '--tmp-dir',
        default='/var/tmp',
        help='Base directory to create temporary files')
    parser.add_argument(
        '-l',
        '--log-level',
        default='INFO',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
                 'N', 'D', 'I', 'W', 'E', 'C'],
        help='Log level')
    parser.add_argument(
        'MKSQUASHFS_OPTIONS',
        nargs=argparse.ZERO_OR_MORE,
        help='Additional command line options for mksquashfs')
    args = parser.parse_args()

    _setup_logging(args.log_level)
    _LOG.info('Started')

    holetree.create(args.SOURCE, args.DESTINATION, args.tmp_dir,
                    args.MKSQUASHFS_OPTIONS)

    _LOG.info('Done!')


if __name__ == "__main__":
    main()
