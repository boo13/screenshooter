# _________________________ Logging setup  _________________________
from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            # "level": 'DEBUG'
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
            # "format": "<green>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</green>",
        },
        {
            "sink": "screenshooter.log",
            "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        },
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)
