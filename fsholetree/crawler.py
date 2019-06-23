import itertools
import logging
import os


_LOG = logging.getLogger(__name__)


def _raise(exc):
    raise exc


def _walk(base_path):
    # Directories should be listed before files inside them.
    return os.walk(base_path, topdown=True, onerror=_raise)


def crawl(base_path):
    yield os.path.curdir, os.lstat(base_path)
    names_n = 1

    for cur_path, dir_names, file_names in _walk(base_path):
        _LOG.info('Descending into \"%s\" (%u)...',
                  cur_path,
                  names_n)

        rel_cur_path = os.path.relpath(cur_path, base_path)
        for basename in itertools.chain(dir_names, file_names):
            rel_path = os.path.join(rel_cur_path, basename)
            full_path = os.path.join(cur_path, basename)

            yield rel_path, os.lstat(full_path)

            names_n += 1

    _LOG.info('Total number of items: %u',
              names_n)
