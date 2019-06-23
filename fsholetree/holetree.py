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

import contextlib
import logging
import os.path
import shutil
import tempfile

import fsholetree.crawler as crawler
import fsholetree.puncher as puncher


_LOG = logging.getLogger(__name__)


@contextlib.contextmanager
def _tmp_dir():
    tmp_dir = tempfile.mkdtemp(suffix='.fsholetree')
    _LOG.debug('Created temp directory \"%s\"', tmp_dir)
    try:
        yield tmp_dir
    finally:
        _LOG.debug('Removing temp directory \"%s\"...', tmp_dir)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        _LOG.debug('Temp directory \"%s\" removed', tmp_dir)


def create(source_dir, destination):
    if not os.path.isdir(source_dir):
        raise RuntimeError('Source \"{}\" is not a directory'.format(
            source_dir))
    if os.path.exists(destination):
        raise RuntimeError('\"{}\" already exists'.format(destination))

    source_dir = os.path.abspath(source_dir)

    with _tmp_dir() as tmp_dir:
        tmp_dir = os.path.abspath(tmp_dir)
        if os.path.commonprefix((source_dir, tmp_dir)) == source_dir:
            raise RuntimeError(
                'Temp directory \"{}\" is inside the source directory \"{}\"'
                .format(tmp_dir, source_dir))

        items = crawler.crawl(source_dir)
        puncher.create_hole_tree_image(items, destination, tmp_dir)
