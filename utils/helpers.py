import logging as log
from random import uniform

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


def round_two_decimal(lower: float, upper: float) -> float:
    """
    Generate a random number between the given lower and upper and round it to two decimal digits.
    :param lower: The lower bound for the random number.
    :param upper: The upper bound for the random number.
    :return: A random number with two decimal digits.
    """

    return round((uniform(lower, upper)), 2)


def element_exist(driver: WebDriver, by: str, element: str) -> bool:
    """
    Check if the specified element exists on the web page.
   :param driver: The WebDriver instance.
   :param by: The method to locate the element ('xpath', 'css_selector', ...).
   :param element: The value to locate the element.
   :return: True if the element exists, False otherwise.
   """

    try:
        driver.find_element(by, element)
        return True
    except NoSuchElementException:
        return False


def convert_path_name(path_name: str) -> str:
    """
    Extracts and returns the name of the file from a specified path.
    :param path_name: The path of the file, including its name.
    :return: The name of the file.
    """

    return path_name.split('/')[-1]


def read_file(name_extension: str) -> str:
    """
    Reads and returns the contents of a specified file.
    :param name_extension: The name of the file, including its extension.
    :return: The data read from the file.
    """

    with open(name_extension, 'r', encoding='utf-8') as file:
        data = file.read()

        log.info(f"A file was read with the name of '{convert_path_name(name_extension)}'.")

        return data


def generate_cache(data: str, name_extension: str) -> None:
    """
    Write data to a cached file specified by the file.
    :param data: The data to be written to the file.
    :param name_extension: The name of the cached file.
    """

    with open(name_extension, 'w', encoding='utf-8', newline='') as file:
        file.write(data)

        log.info(f"A cache file was generated with the name of '{convert_path_name(name_extension)}'.")


def extract_element(element: callable) -> str:
    """
    Extracts a specific attribute or text using the provided callable.
    :param element: A callable that returns the desired data.
    :return: The extracted data as a string. If the data doesn't exist, returns an empty string.
    """

    try:
        _ = element() or ''
        return _.strip()
    except IndexError:
        return ''
