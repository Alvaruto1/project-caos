import os
from flask import Flask
from src.core.exceptions import ConfigDictionary

_DEVELOPMENT = "development"
_DEBUG = "DEBUG"
_PRODUCTION = "PRODUCTION"
_HOST = "host"
_PORT = "port"

def start_webapp(app: Flask, mode:str=_DEVELOPMENT, config_dict:dict={}) -> None:
    """Method that starts the flask app
        e.g.
            start_webapp(app=myApp, mode="DEBUG")
    """
    if mode == _DEVELOPMENT:
        os.environ["FLASK_ENV"] = _DEVELOPMENT
        app.run(host="127.0.0.1", port="8080", debug=True)

    elif mode == _DEBUG:
        if _DEBUG not in config_dict:
            raise ConfigDictionary("Missing '{0}' key in the config dictionary".format(_DEBUG))
        if _HOST not in config_dict[_DEBUG] or _PORT not in config_dict[_DEBUG]:
            raise ConfigDictionary("Missing '{0}' or '{1}' key in the config dictionary".format(_HOST, _PORT))
        
        app.run(host=config_dict[_DEBUG][_HOST], port=config_dict[_DEBUG][_PORT], debug=True)

    elif mode == _PRODUCTION:        
        if _PRODUCTION not in config_dict:
            raise ConfigDictionary("Missing '{0}' key in the config dictionary".format(_DEBUG))
        if  _PORT not in config_dict[_PRODUCTION]:
            raise ConfigDictionary("Missing '{0}' key in the config dictionary".format(_PORT))

        app.run(host="0.0.0.0", port=config_dict[_PRODUCTION][_PORT])
    