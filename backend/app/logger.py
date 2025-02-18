import logging.config
import yaml


with open("logging_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)


logger = logging.getLogger("pinterest_api_logger")
