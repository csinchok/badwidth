import argparse
import logging
import sqlite3

from .tests import iter_stats
from .db import create, save_stats


def main():

    logger = logging.getLogger('badwidth')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[{asctime}] {message}', style='{')
    handler.setFormatter(formatter)

    parser = argparse.ArgumentParser(description='Bandwith tests')
    parser.add_argument('--quiet', dest='quiet', action='store_const', const=True, default=False)
    parser.add_argument('--save', dest='save', action='store_const', const=True, default=False)
    parser.add_argument('--db', dest='db_path', type=str, default='badwidth.sqlite3')

    args = parser.parse_args()
    if args.quiet:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.DEBUG)    

    logger.addHandler(handler)
    logger.info('Starting tests...')

    conn = sqlite3.connect(args.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    create(conn)  # Create the DB, if necessary

    stats = list(iter_stats())
    if args.save:
        sate_stats(conn, stats=stats)
