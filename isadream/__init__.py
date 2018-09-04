import os
import json
import logging

config_path = os.path.join(os.path.dirname(__file__), "../config.json")

with open(config_path, "r") as json_config:
    config = json.load(json_config)

config_env = os.environ.get("DREAM_CONFIG", "TESTING")

if config_env == "TESTING":
    demo_path = os.path.dirname(os.path.dirname(__file__))
    demos = config['JSON_DEMOS']
    config["TESTING"]["BASE_PATH"] = os.path.join(demo_path, config["TESTING"]["BASE_PATH"])

config = config[config_env]

logging.basicConfig(filename='isadream.log', level=config["LOG_LEVEL"])
