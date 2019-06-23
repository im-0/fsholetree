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
