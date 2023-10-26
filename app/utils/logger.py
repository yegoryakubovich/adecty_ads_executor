#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def configure_logger(capture_exceptions: bool = False) -> None:
    logger.remove()
    level = "INFO"
    logger.add("logs/log_{time:YYYY-MM-DD}.log", rotation="12:00",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}", level="INFO",
               encoding="utf-8", compression="zip")
    logger.add(sys.stdout, colorize=True,
               format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {file}:{line} | "
                      "{message}",
               level=level)
    if capture_exceptions:
        logger.add("logs/error_log_{time:YYYY-MM-DD}.log", rotation="12:00",
                   format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}", level="ERROR",
                   encoding="utf-8", compression="zip")

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.disable("telethon")
    logger.disable("os")
    logger.disable("pyrogram")
    logger.disable("httpx")
