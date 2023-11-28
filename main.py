from init import conf
import logging as log

from utils import read_file, generate_cache
from utils import Driver
from app.logics import Extractor
from app.logics import Cleaner
from app.logics import Segmentor
from app.logics import Exporter

# Configuration paths
PATH = {
    'driver': None,  # Selenium Cache Path '~/.cache/selenium/', Set 'None' for auto download.
    'log': 'logs/driver.log',
    'cache': 'cache/dirty.cache',

    'out': {
        'database': 'outs/clean.sqlite3',
        'CSV': 'outs/clean.csv'
    }
}

# Configuration config
CONFIG = {
    'setting': {
        'name': 'setting',
        'browser': 'browser_name'
    },

    'in': {
        'name': 'input',
        'usl': 'usl_address',
        'count': 'count_number'
    },

    'out': {
        'name': 'output',
        'database': 'database_status',
        'csv': 'csv_status'
    }
}

if __name__ == '__main__':

    try:
        driver = Driver(browser=conf.get(CONFIG['setting']['name'], CONFIG['setting']['browser']), executable_path=PATH['driver'], log_path=PATH['log'])

        if conf.get(CONFIG['in']['name'], CONFIG['in']['usl']) == 'None':
            log.info('Dirty data was loaded from the cached file (A text in HTML format of all the data to be cleared).')
            data = read_file(name_extension=PATH['cache'])
        else:
            extractor = Extractor(driver=driver.run(), url=conf.get(CONFIG['in']['name'], CONFIG['in']['usl']), count=conf.getint(CONFIG['in']['name'], CONFIG['in']['count']))
            data = extractor.run()

        if not (conf.getboolean(CONFIG['out']['name'], CONFIG['out']['database']) and conf.getboolean(CONFIG['out']['name'], CONFIG['out']['csv'])):
            generate_cache(data, name_extension=PATH['cache'])
        else:
            cleaner = Cleaner(data=data)
            segmentor = Segmentor(data=cleaner.run())
            exporter = Exporter(data=segmentor.run())
            if conf.getboolean(CONFIG['out']['name'], CONFIG['out']['database']):
                exporter.database(name_extension=PATH['out']['database'])
            if conf.getboolean(CONFIG['out']['name'], CONFIG['out']['csv']):
                exporter.csv(name_extension=PATH['out']['CSV'])

    except Exception:
        log.critical("During the execution of the program in the 'main file', an issue was encountered.", exc_info=True)
        raise SystemExit("Exception: 'main file', More information in the log file.")
