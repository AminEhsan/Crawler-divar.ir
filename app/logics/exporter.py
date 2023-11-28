import logging as log
from typing import List
from csv import DictWriter

from utils import convert_path_name, Database
from app.interfaces import Base


class Exporter(Base):
    """
    Divides the data into distinct segments and exports them.
    :param data: A list of BeautifulSoup objects containing the data to be segmented and exported.
    """

    __options = {
        'names': {
            'table': 'Clean'
        },
        'fields': {
            'database': '''
                        ID            INTEGER NOT NULL UNIQUE,
                        Title         TEXT    NOT NULL,
                        Description_1 TEXT    NOT NULL,
                        Description_2 TEXT    NOT NULL,
                        Type          TEXT    NOT NULL,
                        Time_Region   TEXT    NOT NULL,
                        Image         TEXT    NOT NULL,
                        Link          TEXT    NOT NULL UNIQUE PRIMARY KEY
                        ''',
            'table': ':ID, :Title, :Description_1, :Description_2, :Type, :Time_Region, :Image, :Link',
            'csv': ['ID', 'Title', 'Description_1', 'Description_2', 'Type', 'Time_Region', 'Image', 'Link']
        }
    }

    def __init__(self, data: List[dict]) -> None:
        log.info(f'{self._class_name()} started.')

        self.__data = data

    def database(self, name_extension) -> None:
        """
        Export the segmented information using a CSV file.
        :param name_extension: The name and extension of the CSV file to create.
        """

        try:
            log.info(f'{self._method_name()} started.')

            db = Database(name_extension=name_extension,
                          sql_init=f'''
                                   DROP TABLE IF EXISTS {self.__options['names']['table']}; 
                                   CREATE TABLE {self.__options['names']['table']}
                                   (
                                        {self.__options['fields']['database']}
                                   );
                                   ''')

            db.exe(sql=f'''
                       INSERT INTO {self.__options['names']['table']}
                       VALUES ({self.__options['fields']['table']});
                       ''',
                   data=self.__data)

            log.info(f'{self._method_name()} ended.')
            log.info(f"A Database file was generated with the name of '{convert_path_name(name_extension)}'.")

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')

    def csv(self, name_extension) -> None:
        """
        Export the segmented information using a CSV file.
        :param name_extension: The name and extension of the CSV file to create.
        """

        try:
            log.info(f'{self._method_name()} started.')

            with open(name_extension, 'w', encoding='utf-8', newline='') as file:
                writer = DictWriter(file, fieldnames=self.__options['fields']['csv'])
                writer.writeheader()
                for _ in self.__data:
                    writer.writerow(_)

                log.info(f'{self._method_name()} ended.')
                log.info(f"A csv file was generated with the name of '{convert_path_name(name_extension)}'.")

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')
