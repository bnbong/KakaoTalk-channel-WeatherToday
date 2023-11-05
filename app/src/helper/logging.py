# --------------------------------------------------------------------------
# Backend Application의 logger을 정의하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging
import logging.handlers

from src.core.settings import AppSettings


LOGGING_FORMAT = (
    "[%(levelname)1.1s "
    "%(asctime)s "
    "P%(process)d "
    "%(threadName)s "
    "%(module)s:%(lineno)d] "
    "%(message)s"
)


def init_logger(root_logger_name: str, app_settings: AppSettings) -> None:
    app_logger_level = (
        logging.DEBUG if app_settings.LOGGING_DEBUG_LEVEL else logging.INFO
    )

    logging.basicConfig(level=app_logger_level, format=LOGGING_FORMAT)
