import logging as log
from typing import List

from bs4 import BeautifulSoup

from utils import extract_element
from app.interfaces import Base, Crawler
from app.exceptions import SelectElementException


class Segmentor(Base, Crawler):
    """
    Divides the data into distinct segments.
    :param data: A list of BeautifulSoup objects containing the data to be segmented.
    """

    __options = {
        'elements': {
            'title': '*[class*="__title"]',
            'description': '*[class*="__description"]',
            'type': '*[class*="__red-text"]',
            'time_region': '*[class*="__bottom-description"]',
            'image': '*[class*="__image"]'
        }
    }

    def __init__(self, data: List[BeautifulSoup]) -> None:
        self.__data = data

        self.__segment = []

    def __segmentor(self) -> None:
        log.info(f'{self._method_name()} started.')

        if not self.__data[0].select(self.__options['elements']['title']):
            raise SelectElementException(self.__options['elements']['title'])
        if not self.__data[0].select(self.__options['elements']['description']):
            raise SelectElementException(self.__options['elements']['description'])
        if not self.__data[0].select(self.__options['elements']['time_region']):
            raise SelectElementException(self.__options['elements']['time_region'])

        counter = 0
        for _ in self.__data:
            counter += 1

            ad = {
                'ID': f'{counter}',
                'Title': extract_element(lambda x=_: x.select(self.__options['elements']['title'])[0].text),
                'Description_1': extract_element(lambda x=_: x.select(self.__options['elements']['description'])[0].text),
                'Description_2': extract_element(lambda x=_: x.select(self.__options['elements']['description'])[1].text),
                'Type': extract_element(lambda x=_: x.select(self.__options['elements']['type'])[0].text),
                'Time_Region': extract_element(lambda x=_: x.select(self.__options['elements']['time_region'])[0].text),
                'Image': extract_element(lambda x=_: x.select(self.__options['elements']['image'])[0].get('data-src')),
                'Link': f'https://divar.ir/v/{_.get("href").split("/")[-1]}'
            }
            self.__segment.append(ad)

        log.info(f'{self._method_name()} ended.')

    def run(self) -> List[dict]:
        """
        :return: A list of dictionaries containing the segmented data: {'ID': '', 'Title': '', 'Description_1': '', 'Description_2': '', 'Type': '', 'Time_Region': '', 'Image': '', 'Link': ''}.
        """

        try:
            log.info(f'{self._class_name()} started.')
            self.__segmentor()

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')
            return self.__segment
