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

import logging
import sys

import fsholetree.holetree as holetree


_LOG = logging.getLogger()


def _setup_logging():
    _LOG.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname).1s] %(message)s')
    handler.setFormatter(formatter)

    _LOG.addHandler(handler)


def main():
    _setup_logging()
    _LOG.info('Started')

    holetree.create(sys.argv[1], sys.argv[2])

    _LOG.info('Done!')


if __name__ == "__main__":
    main()
