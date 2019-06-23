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

import itertools
import logging
import os
import stat


_LOG = logging.getLogger(__name__)


def _raise(exc):
    raise exc


def _walk(base_path):
    # Directories should be listed before files inside them.
    return os.walk(base_path, topdown=True, onerror=_raise)


def crawl(base_path):
    yield os.path.curdir, os.lstat(base_path), None
    names_n = 1

    for cur_path, dir_names, file_names in _walk(base_path):
        _LOG.info('Descending into \"%s\" (%u)...',
                  cur_path,
                  names_n)

        rel_cur_path = os.path.relpath(cur_path, base_path)
        for basename in itertools.chain(dir_names, file_names):
            rel_path = os.path.join(rel_cur_path, basename)
            full_path = os.path.join(cur_path, basename)

            stat_data = os.lstat(full_path)
            link_path = os.readlink(full_path) \
                if stat.S_ISLNK(stat_data.st_mode) \
                else None
            yield rel_path, stat_data, link_path

            names_n += 1

    _LOG.info('Total number of items: %u',
              names_n)
