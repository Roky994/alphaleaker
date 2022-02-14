#!/usr/bin/python
import logging
import os

from dotenv import load_dotenv


load_dotenv()
LOG_FILE = os.getenv("LOG_FILE")

from internal.tweets import service as tweets_service

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

    logger.info("Running Tweets.")
    tweets_service.TweetsService().report()
