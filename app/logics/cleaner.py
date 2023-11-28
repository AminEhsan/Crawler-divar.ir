import logging as log
from typing import List
from json import loads

from bs4 import BeautifulSoup

from utils import generate_cache
from app.interfaces import Base, Crawler
from app.exceptions import SelectElementException


class Cleaner(Base, Crawler):
    """
    Cleaner specific elements from dirty data using BeautifulSoup.
    :param data: Dirty data (A text in HTML format of all the data to be cleared).
    """

    __options = {
        'elements': {
            'ad': 'a[href*="/v/"]'
        }
    }

    def __init__(self, data: str) -> None:
        self.__data = data

        self.__soup = None
        self.__information = []
        self.__clean = []

    def __cleaner(self) -> None:
        log.info(f'{self._method_name()} started.')
        self.__soup = BeautifulSoup(self.__data, 'html.parser')

        self.__information = loads(self.__soup.select("title")[0].text)
        log.info(f"Data information >>  Name: '{self.__information['name']}', Date: '{self.__information['date']}', Count: '{self.__information['count']}', URL: '{self.__information['url']}'.")

        if not self.__soup.select(self.__options['elements']['ad']):
            raise SelectElementException(self.__options['elements']['ad'])
        ad = self.__soup.select(self.__options['elements']['ad'])

        temp = set()
        for _ in ad:

            unique = _.get("href").split("/")[-1]
            if unique not in temp:
                temp.add(unique)
                self.__clean.append(_)

        log.info(f'{self._method_name()} ended.')
        log.info(f"Number of elements found 'All: {len(ad)} - Unique: {len(self.__clean)}'.")

    def run(self) -> List[BeautifulSoup]:
        """
        If an exception is encountered, the input data is cached.
        :return: A list of BeautifulSoup objects containing cleaned data.
        """

        try:
            log.info(f'{self._class_name()} started.')
            self.__cleaner()

        except Exception:
            generate_cache(self.__data, name_extension='')
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')
            return self.__clean
