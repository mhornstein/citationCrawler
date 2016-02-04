import ConfigParser
import sys

def load_config():
    try:
        config_file = sys.argv[1]
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        config.eval = lambda sec,key: eval(config.get(sec,key))
        config.getfilename = lambda: config_file
        return config
    except:
        exit(-1)

if __name__ == '__main__':
    config = load_config()
    pass