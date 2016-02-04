import ConfigParser
import sys
from sqlite_connector import *

Base = declarative_base()

def load_config():
    try:
        config_file = sys.argv[1]
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        config.eval = lambda sec,key: eval(config.get(sec,key))
        config.getfilename = lambda: config_file
        return config
    except Exception as e:
        exit(-1)

if __name__ == '__main__':
    config = load_config()
    sqlite_connector = sqliteConnector(config.get("DB", "DB_path"), config.get("DB", "DB_path_to_extensions"))