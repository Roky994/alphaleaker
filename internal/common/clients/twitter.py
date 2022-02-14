import datetime
import logging
import os

from dotenv import load_dotenv

import requests

logger = logging.getLogger(__name__)


class TwitterClientError(Exception):
    pass


class TwitterClient:
    API_URL = "https://api.twitter.com/2"  # API v2
    OK_STATUS_CODES = [200]

    _bearer_token = None

    def __init__(self) -> None:
        load_dotenv()
        self._bearer_token = os.getenv("TWITTER_BEARER")

    def _request(self, method: str, url: str, params: dict = None) -> str:
        response = requests.request(
            method,
            url="{}{}".format(self.API_URL, url),
            headers={"authorization": "Bearer {}".format(self._bearer_token)},
            params=params,
        )

        if response.status_code not in self.OK_STATUS_CODES:
            logger.error("API call failed: {}.".format(response.content))
            raise TwitterClientError(
                "API call failed with code {}".format(response.status_code)
            )

        return response.json()

    def get_user_tweets(
        self, user_id: int, datetime_from: datetime.datetime = None
    ) -> str:
        params = {}
        if datetime_from:
            params["start_time"] = datetime_from.strftime("%Y-%m-%dT%H:%M:%SZ")

        return self._request(
            "GET",
            url="/users/{user_id}/tweets".format(user_id=user_id),
            params=params,
        )
