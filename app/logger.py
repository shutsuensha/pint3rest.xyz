import logging.config

import yaml

from app.config import settings

with open("logging_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


config["handlers"]["file"]["filename"] = settings.LOGS_PATH + "server_errors.log"

logging.config.dictConfig(config)

logger = logging.getLogger("pinterest_api_logger")
