import logging as log
import sqlite3 as db

from app.interfaces import Base


class Database(Base):
    """
    This is a database handler class for SQLite. It provides methods to connect to the database, execute SQL commands, and fetch results.
    :param name_extension: The name and extension of the SQLite database file.
    :param sql_init: The initial SQL statement(s) to execute when the database is created.
    """

    def __init__(self, name_extension: str, sql_init: str = None) -> None:
        log.info(f'{self._class_name()} started.')

        self.__name = name_extension

        self.__conn = None
        self.__cursor = None

        if sql_init:
            self.exe(sql_init)

    def __connect(self) -> None:
        if self.__conn is None:
            self.__conn = db.connect(self.__name)
            self.__cursor = self.__conn.cursor()
            log.info(f'Connected to the database {self.__name}.')

    def __disconnect(self) -> None:
        if self.__conn:
            self.__cursor.close()
            self.__conn.close()
            self.__conn = None
            log.info(f'Disconnected from the database {self.__name}.')

    def __execute(self, sql: str, data: None | dict | list) -> None:
        if data is None:
            self.__cursor.executescript(sql)
        elif isinstance(data, dict):
            self.__cursor.execute(sql, data)
        elif isinstance(data, list):
            self.__cursor.executemany(sql, data)
        else:
            raise ValueError(f"Invalid data type for the 'data' parameter in the {self._method_name()}.")

    def exe(self, sql: str, data: dict | list = None) -> None:
        """
        Execute an SQL query with optional data.
        :param sql: The SQL query to execute.
        :param data: Optional data for parameterized queries (default is None).
        """

        try:
            log.info(f'{self._method_name()} started.')

            self.__connect()
            self.__execute(sql, data)
            self.__conn.commit()

            log.info(f'{self._method_name()} ended.')

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')

        finally:
            self.__disconnect()

    def get(self, sql: str, data: None | dict | list = None) -> list:
        """
        Execute an SQL SELECT query with optional data and return the results as a list.
        :param sql: The SQL SELECT query to execute.
        :param data: Optional data for parameterized queries (default is None).
        :return: A list of query results.
        """

        try:
            log.info(f'{self._method_name()} started.')

            self.__connect()
            self.__execute(sql, data)
            result = self.__cursor.fetchall()

            log.info(f'{self._method_name()} ended.')

        except Exception:
            log.critical(f"During the execution of the program in the '{self._class_name()}', an issue was encountered.", exc_info=True)
            raise SystemExit(f"Exception: '{self._class_name()}', More information in the log file.")

        else:
            log.info(f'{self._class_name()} finished.')
            return result

        finally:
            self.__disconnect()
