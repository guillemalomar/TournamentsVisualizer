import conda
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

import src.settings as settings
from mpl_toolkits.basemap import Basemap


def create_plot(text, csv_file_name, image_file_name):
    try:
        data = pd.read_csv(csv_file_name, sep=";")
        plt.figure(figsize=(settings.WIDTH_DPI / settings.DPI, settings.HEIGHT_DPI / settings.DPI), dpi=settings.DPI)

        m = Basemap(llcrnrlon=-11, llcrnrlat=25, urcrnrlon=24, urcrnrlat=65)
        m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
        m.fillcontinents(color='grey', alpha=0.3)
        m.drawcoastlines(linewidth=0.1, color="white")

        data['labels_enc'] = pd.factorize(data['homecontinent'])[0]

        m.scatter(data['homelon'], data['homelat'], s=data['n'] / 6, alpha=0.4, c=data['labels_enc'], cmap="Set1")

        plt.text(-5, 32,
                 str(text) + '\n\nEuropean Oldschool Tournaments in 2019',
                 ha='left', va='bottom', size=30, color='#555555')

        plt.savefig(image_file_name, bbox_inches='tight')
        logging.info(settings.MESSAGES['MAP_SUCCESS'].format(image_file_name))
    except Exception as exc:
        logging.error(settings.MESSAGES['MAP_ERROR'].format(image_file_name, exc))
        raise exc
