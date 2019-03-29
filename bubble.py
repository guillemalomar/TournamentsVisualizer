import argparse
import logging
import sys

import src.settings as settings
from src.data_parser import DataParser
from src.settings.logger import set_logger

set_logger()


def create_maps(do_global=True, parser=None, keyword=None, file=None):
    my_data_parser = DataParser(file)

    if do_global:
        my_data_parser.obtain_all()

    if parser and keyword:
        my_data_parser.obtain_by_keyword_and_parser(keyword, parser)
    elif parser:
        my_data_parser.obtain_by_parser(parser)
    elif keyword:
        my_data_parser.obtain_by_keyword(keyword)


def args_handler(argv):

    p = argparse.ArgumentParser(
        description='Jobs map creator',
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument('-p', '--parser', action='store', type=int, default=None,
                   help='The parser id that you want to check.')
    p.add_argument('-k', '--keyword', action='store', type=str, default=None,
                   help='The keyword that you want to check.')
    p.add_argument('-ng', '--noglobal', action='store_true', dest='avoid_global',
                   help='Deactivate the global map.')
    p.add_argument('-f', '--file', action='store', type=str, default=None,
                   help='CSV input file. If not specified it will generate it from the MYSQL data.')
    return p.parse_args(argv[1:])


def _main(argv):
    args = args_handler(argv)

    if args.file and (args.parser or args.keyword):
        logging.error(settings.MESSAGES['WRONG_FILE_MODE'])
        sys.exit()

    if args.file:
        try:
            f = open(args.file, 'r')
            f.close()
        except FileNotFoundError:
            logging.error(settings.MESSAGES['FILE_NOT_FOUND'])
            sys.exit()

    if args.avoid_global:
        do_global = False
    else:
        do_global = True

    create_maps(do_global, args.parser, args.keyword, args.file)


if __name__ == '__main__':
    _main(sys.argv)
