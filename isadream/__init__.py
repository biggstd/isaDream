import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

config_env = os.environ.get("DREAM_CONFIG", "TESTING")

DATA_MOUNT = config[config_env]["DATA_MOUNT"]
