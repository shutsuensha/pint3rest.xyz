import logging.config
import yaml

# Загрузка конфигурации из YAML файла
with open("logging_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

# Использование логгера
logger = logging.getLogger("pinterest_api_logger")
