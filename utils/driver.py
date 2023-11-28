import logging as log

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService

from app.interfaces import Base, Crawler


class Driver(Base, Crawler):
    """
    WebDriver manager for different browsers.
    :param browser: The browser to use ('Chrome' or 'Firefox').
    :param executable_path: Path to the executable of the WebDriver, Set 'None' for auto download.
    :param log_path: Path to the log file where WebDriver logs will be saved.
    """

    __options = {
        'browser': {
            'chrome': 'Chrome',
            'firefox': 'Firefox'
        }
    }

    def __init__(self, browser: str, executable_path: str | None, log_path: str) -> None:
        self.__browser = browser
        self.__executable_path = executable_path
        self.__log_path = log_path

        self.__driver = None  # The Selenium WebDriver instance.

    def __driving(self):
        if self.__browser == self.__options['browser']['chrome']:
            service = ChromeService(executable_path=self.__executable_path, log_path=self.__log_path)
            self.__driver = webdriver.Chrome(service=service)
            log.info(f"The selected browser is '{self.__options['browser']['chrome']}'.")

        elif self.__browser == self.__options['browser']['firefox']:
            service = FirefoxService(executable_path=self.__executable_path, log_path=self.__log_path)
            self.__driver = webdriver.Firefox(service=service)
            log.info(f"The selected browser is '{self.__options['browser']['firefox']}'.")

        else:
            raise ValueError(f"Invalid browser type: '{self.__browser}'.")

    def run(self) -> webdriver:
        """:return: The initialized WebDriver instance."""

        try:
            log.info(f'{self._class_name()} started.')
            self.__driving()

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            if self.__driver:
                self.__driver.quit()
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')
            return self.__driver
