import logging

from src.utils.csv_wrapper import CSVWrapper
from src.utils.plot_wrapper import create_plot
from src.utils.date_formatter import obtain_time
from src.settings import MESSAGES


class DataParser(object):

    def __init__(self, file_name=None):

        if file_name:
            current_file = file_name
            self.from_file = True
            self.csv_wrapper = CSVWrapper(current_file, False)
            self.file_dest = current_file
            self.image_dest = current_file[:-4] + '.png'
        else:
            current_file = obtain_time() + '.csv'
            self.from_file = False
            self.csv_wrapper = CSVWrapper('data/csvs/' + current_file, True)
            self.file_dest = 'data/csvs/' + current_file
            self.image_dest = 'data/images/' + current_file[:-4] + '.png'

    def obtain_all(self):
        if not self.from_file:
            self.csv_wrapper.create_csv()
        try:
            create_plot("Locations",
                        self.file_dest,
                        self.image_dest)
            print(MESSAGES['MAP_SUCCESS'].format(self.image_dest))
            logging.info(MESSAGES['MAP_SUCCESS'].format(self.image_dest))
        except Exception as exc:
            print(MESSAGES['MAP_ERROR'].format('global', exc))
            logging.error(MESSAGES['MAP_ERROR'].format('global', exc))

    def obtain_by_keyword(self, keyword):
        if not self.from_file:
            self.csv_wrapper.create_csv(kw=keyword)
        try:
            create_plot(keyword,
                        self.file_dest[:-4] + '_' + keyword + '.csv',
                        self.image_dest[:-4] + '_' + keyword + '.png')
            print(MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + keyword + '.png'))
            logging.info(MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + keyword + '.png'))
        except Exception as exc:
            print(MESSAGES['MAP_ERROR'].format('keyword', exc))
            logging.error(MESSAGES['MAP_ERROR'].format('keyword', exc))

    def obtain_by_parser(self, parser_id):
        if not self.from_file:
            self.csv_wrapper.create_csv(parser=parser_id)
        try:
            create_plot(parser_id,
                        self.file_dest[:-4] + '_' + str(parser_id) + '.csv',
                        self.image_dest[:-4] + '_' + str(parser_id) + '.png')
            print(MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + str(parser_id) + '.png'))
            logging.info(MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + str(parser_id) + '.png'))
        except Exception as exc:
            print(MESSAGES['MAP_ERROR'].format('parser', exc))
            logging.error(MESSAGES['MAP_ERROR'].format('parser', exc))

    def obtain_by_keyword_and_parser(self, kw, parser_id):
        if not self.from_file:
            self.csv_wrapper.create_csv(kw=kw, parser=parser_id)
        try:
            create_plot(parser_id,
                        self.file_dest[:-4] + '_' + str(parser_id) + '_' + str(kw) + '.csv',
                        self.image_dest[:-4] + '_' + str(parser_id) + '_' + str(kw) + '.png')
            print(
                MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + str(parser_id) + '_' + str(kw) + '.png'))
            logging.info(
                MESSAGES['MAP_SUCCESS'].format(self.image_dest[:-4] + '_' + str(parser_id) + '_' + str(kw) + '.png'))
        except Exception as exc:
            print(MESSAGES['MAP_ERROR'].format('parser and kw', exc))
            logging.error(MESSAGES['MAP_ERROR'].format('parser and kw', exc))
