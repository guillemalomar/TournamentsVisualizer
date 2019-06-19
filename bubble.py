import argparse
import logging
import sys

import src.settings as settings
from src.data_parser import DataParser
from src.settings.logger import set_logger

set_logger()


def create_maps(file=None, month=None):
    if month:
        my_data_parser = DataParser(file, month)
        my_data_parser.obtain_by_date(month)
    else:
        my_data_parser = DataParser(file)
        my_data_parser.obtain_all()


def args_handler(argv):

    p = argparse.ArgumentParser(
        description='Tournaments Visualizer',
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument('-f', '--file', action='store', type=str, default=None,
                   help='CSV input file. If not specified it will generate it from the MYSQL data.')

    p.add_argument('-m', '--month', action='store', type=int, default=None,
                   help='Month that the data will be obtained from.')
    return p.parse_args(argv[1:])


def _main(argv):
    args = args_handler(argv)

    if args.file:
        try:
            f = open(args.file, 'r')
            f.close()
        except FileNotFoundError:
            logging.error(settings.MESSAGES['FILE_NOT_FOUND'])
            sys.exit()

    if args.month:
        create_maps(args.file, args.month)
    else:
        create_maps(args.file)


if __name__ == '__main__':
    _main(sys.argv)
