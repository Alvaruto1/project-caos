"""DO NOT EDIT THIS FILE"""

import sys
from config import environments_config_dict
from src.webapp.controllers import *
from src.core import (
    start_webapp,
    _DEBUG,
    _PRODUCTION,
    _DEVELOPMENT
)
from src.utils.temp_toke import PerpetualTimer
from src.db.DAO.mysqlDAO import DAOManagerMysql

perpetualT = PerpetualTimer()
perpetualT.setTime(100)
d = DAOManagerMysql()
d.init()

if __name__ == "__main__":
    start_arguments = sys.argv[1:]
    start_mode = start_arguments[0].upper() if len(start_arguments) >=1 else _DEVELOPMENT

    if start_mode == _DEBUG:
        start_webapp(mode=_DEBUG, config_dict=environments_config_dict)
    elif start_mode == _PRODUCTION:
        start_webapp(mode=_PRODUCTION, config_dict=environments_config_dict)
    elif start_mode == _DEVELOPMENT:
        start_webapp(mode=_DEVELOPMENT)