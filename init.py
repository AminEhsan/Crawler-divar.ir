"""
This file is responsible for managing crucial program settings and configurations.
(Import and use this file at the program's starting point for essential configurations)
"""

import logging as log
import logging.config as log_conf
from configparser import ConfigParser

# Configuration paths
PATH = {
    'log': 'logs/general.log',

    'conf': {
        'general': 'confs/general.ini',
        'logging': 'confs/logging.ini'
    }
}

try:
    conf = ConfigParser()  # Initialize the ConfigParser
    conf.read(filenames=PATH['conf']['general'])  # Read the general configuration file

    log_conf.fileConfig(fname=PATH['conf']['logging'], defaults={'filename': PATH['log']})  # Configure logging based on the logging configuration file

except Exception:
    log.critical("During the execution of the program in the 'init file', an issue was encountered.", exc_info=True)
    raise SystemExit("Exception: 'init file', More information in the log file.")
