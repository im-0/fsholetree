import logging
import sys

import fsholetree.crawler as crawler
import fsholetree.puncher as puncher


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

    puncher.create_hole_tree_image(crawler.crawl(sys.argv[1]), sys.argv[2])

    _LOG.info('Done!')


if __name__ == "__main__":
    main()
