"""
TabWorking -- Load data from the Worksheet 2 tab
"""

from typing import List, Dict
from loguru import logger
import pandas as pd
from urllib.request import urlopen
import json
import numpy as np
import re
import os
import requests
import socket
import io

import data_convert.udatetime
from data_convert.worksheet_wrapper import WorksheetWrapper
from data_convert.tab_base import TabBase
from data_convert.tab_cleaner import TabCleaner


class TabWorking(TabBase):

    def __init__(self):
        super(TabWorking, self).__init__()

        # worksheet dates from top row
        self.last_publish_time = ""
        self.last_push_time = ""
        self.current_time = ""


    def parse_dates(self, dates: List):
        if len(dates) != 5:
            raise Exception("First row layout (containing dates) changed")
        last_publish_label, last_publish_value, last_push_label, \
            last_push_value, current_time_field = dates

        if last_publish_label != "Last Publish Time:":
            raise Exception("Last Publish Time (cells V1:U1) moved")
        if last_push_label != "Last Push Time:":
            raise Exception("Last Push Time (cells Z1:AA1) moved")
        if not current_time_field.startswith("CURRENT TIME: "):
            raise Exception("CURRENT TIME (cell AG1) moved")

        self.last_publish_time = last_publish_value
        self.last_push_time = last_push_value
        self.current_time = current_time_field[current_time_field.index(":")+1:].strip()


    def _load_metadata(self) -> pd.DataFrame:
        xdir = os.path.dirname(__file__)
        xpath = os.path.join(xdir, "meta_working.json")
        if not os.path.exists(xpath):
            raise Exception(f"Missing meta-data file: {xpath}")
        return pd.read_json(xpath)


    def _load_content(self) -> pd.DataFrame:
        """Load the working (unpublished) data from google sheets"""

        gs = WorksheetWrapper()
        url = gs.get_sheet_url("working")

        df = gs.download_data(url)
        
        dates = gs.read_as_list(df, "W1:AN1", ignore_blank_cells=True, single_row=True)
        self.parse_dates(dates)

        df = gs.read_as_frame(df, "A2:BR60", header_rows=1)

        # cleanup logic
        cleaner = TabCleaner()
        cleaner.cleanup_names(df)

        df_meta_data = self.metadata()
        if df_meta_data is None:
            raise Exception("Meta-data not available")

        df_changed = cleaner.find_changes(df, df_meta_data)
        if not (df_changed is None):
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 200)
            logger.error(f"Names are\n{df_changed}")
            raise Exception("Meta-data is out-of-date")

        df = cleaner.remap_names(df, df_meta_data)

        #cleaner.convert_types(df, df_meta_data)

        df = df[ df.state != ""]
        return df


# ------------------------------------------------------------
def main():

    tab = TabWorking()
    tab.load()

    logger.info(f"working\n{tab.df.to_json(orient='table', indent=2)}")


if __name__ == '__main__':
    main()
