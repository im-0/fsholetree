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
