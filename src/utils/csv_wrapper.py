import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from src.settings import GEO_TIMEOUT
from src.settings import MESSAGES
from src.utils.mysql_wrapper import MysqlWrapper


class CSVWrapper(object):
    def __init__(self, csv_name, mysql=True):

        if mysql:
            self.sql_wrapper = MysqlWrapper()
            self.sql_wrapper.connect()
        self.csv_name = csv_name
        self.locations = {}

    def create_csv(self, filter_name=None, value=None):

        csv_file = self.csv_name
        if not filter_name:
            locations = self.sql_wrapper.select_all()
        else:  # filter = 'date'
            locations = self.sql_wrapper.select_filter_by_time(value)

        geo_locator = Nominatim(timeout=GEO_TIMEOUT)
        my_file = open(csv_file, 'w')
        my_file.write('homelon;homelat;homecontinent;n;color\n')
        for loc in locations:
            loc_name = loc[0]
            loc_value = loc[1]
            try:
                loc_color = obtain_color(loc[2])
            except:
                loc_color = 'NoRules'
            if loc_name != ' ':
                if loc_name not in self.locations:
                    tries = 0
                    while True:
                        try:
                            location = geo_locator.geocode(loc_name)
                            self.locations[loc_name] = (str(location.longitude), str(location.latitude))
                            break
                        except GeocoderTimedOut as exc:
                            logging.debug(MESSAGES['GEO_ERROR'].format(loc_name, exc))
                            tries += 1
                            if tries == 3:
                                continue
                try:
                    my_file.write(";".join([self.locations[loc_name][0],
                                            self.locations[loc_name][1],
                                            loc_name,
                                            str(int(loc_value.real * 100)),
                                            loc_color]) + '\n')
                except Exception as exc:
                    logging.error(MESSAGES['CSV_ERROR'].format(csv_file, exc))
                    raise exc
        logging.info(MESSAGES['CSV_SUCCESS'].format(csv_file))
        my_file.close()


def obtain_color(rule):
    if rule == 'Swedish':
        return '0'
    elif rule == 'EC':
        return '20'
    elif rule == 'Ravenna':
        return '7'
    else:
        return '14'
