#!/usr/bin/python
import logging
import os
import sys

from dotenv import load_dotenv


load_dotenv()
LOG_FILE = os.getenv("LOG_FILE")

from internal.core import db
from internal.main import service

logger = logging.getLogger(__name__)


def _init_logging() -> None:
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s: %(message)s",
        datefmt="%Y-%d-%m %H:%M:%S",
    )


if __name__ == "__main__":
    _init_logging()

    quiet = False
    if len(sys.argv) > 1:
        if "migrate" in sys.argv:
            drop_tables = "drop" in sys.argv
            logger.info("Running migrations (drop={}).".format(drop_tables))
            db.migrate(drop=drop_tables)
            exit(0)

        if "quiet" in sys.argv:
            quiet = True

    logger.info("Running TrendingCryptoCurrencies (quiet_mode={}).".format(quiet))
    service.TrendingCryptoCurrencies(quiet=quiet).report()
