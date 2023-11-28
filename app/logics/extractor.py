import logging as log
from time import sleep
from json import dumps
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from htmlmin import minify

from utils import element_exist, round_two_decimal
from app.interfaces import Base, Crawler
from app.exceptions import SelectElementException


class Extractor(Base, Crawler):
    """
    Extract data from the specified URL using Selenium WebDriver.
    :param driver: The Selenium WebDriver instance.
    :param url: The URL to extract data from.
    :param count: Maximum number of scrolls for data extraction.
    """

    __options = {
        'elements': {
            'export': '//div[contains(@class, "browse-post-list")]',
            'unstable': '//*[contains(@class, "post-list__unsafe-bottom-container")]/*',
            'load': '//*[contains(@class, "kt-progress-circular__content")]',
            'try': '//button[contains(@class, "error-message__button")]'
        }
    }

    def __init__(self, driver: webdriver, url: str, count: int) -> None:
        self.__driver = driver
        self.__url = url
        self.__count = count

        self.__data = ''

    def __exporter(self) -> None:
        if not element_exist(self.__driver, By.XPATH, self.__options['elements']['export']):
            raise SelectElementException(self.__options['elements']['export'])
        chunk_data = self.__driver.find_element(By.XPATH, self.__options['elements']['export']).get_attribute('innerHTML')
        self.__data += minify(chunk_data, remove_comments=True, remove_all_empty_space=True)

    def __height(self) -> int:
        code = 'return document.body.scrollHeight;'
        return self.__driver.execute_script(code)

    def __downer(self) -> None:
        code = 'window.scrollBy({top: document.body.scrollHeight, behavior: "smooth"});'
        self.__driver.execute_script(code)

    def __unstable_check(self) -> None:
        if element_exist(self.__driver, By.XPATH, self.__options['elements']['unstable']):
            log.warning("Data extraction is slow 'likely due to an unstable connection'.")

            exists_load = element_exist(self.__driver, By.XPATH, self.__options['elements']['load'])
            exists_try = element_exist(self.__driver, By.XPATH, self.__options['elements']['try'])
            if not (exists_load or exists_try):
                raise SelectElementException(f'{self.__options["elements"]["load"]} or {self.__options["elements"]["try"]}')

        if element_exist(self.__driver, By.XPATH, self.__options['elements']['load']):
            log.info('Please wait while the content is loading.')
            sleep(10)

    def __data_load(self) -> None:
        sleep(round_two_decimal(1, 2))
        log.warning("The (try button) was clicked 'due to a probable unstable connection'.")
        self.__driver.find_element(By.XPATH, self.__options['elements']['try']).click()

    def __scroller(self) -> None:
        log.info(f'{self._method_name()} started.')
        last = self.__height()

        counter = 0
        while True:
            counter += 1
            self.__exporter()
            self.__downer()
            log.info(f'Scroll count: {counter}.')
            sleep(round_two_decimal(1, 2))

            self.__unstable_check()

            new = self.__height()

            if new == last:
                if element_exist(self.__driver, By.XPATH, self.__options['elements']['try']):
                    self.__data_load()
                else:
                    log.info(f'{self._method_name()} ended.')
                    break

            if self.__count and self.__count == counter:
                log.info(f"{self._method_name()} ended 'due to reaching the maximum scroll count'.")
                break

            last = new

    def run(self) -> str:
        """:return: A text in HTML format of all the data to be cleared."""

        try:
            log.info(f'{self._class_name()} started.')
            self.__driver.implicitly_wait(1)
            log.info(f'URL: {self.__url}.')

            self.__driver.maximize_window()
            log.warning('Refrain from closing the window, resizing, or scrolling the browser.')
            self.__driver.get(self.__url)

            self.__scroller()

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')

            title = dumps({'name': 'Dirty Data', 'date': str(datetime.now()), 'count': self.__count, "url": self.__url})
            return f'<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>{title}</title></head><body><main>{self.__data}</main></body></html>'

        finally:
            self.__driver.quit()
