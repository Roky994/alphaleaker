import logging
import os

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


load_dotenv()
DISCORD_SECRET = os.getenv("DISCORD_WEBHOOK_SECRET")


class DiscordWebhookClientError(Exception):
    pass


class DiscordWebhookClient:
    BASE_DISCORD_URL = "https://discord.com/api/webhooks"
    OK_STATUS_CODES = [204]

    def _request(self, message: str) -> None:
        response = requests.post(
            "{}/{}".format(self.BASE_DISCORD_URL, DISCORD_SECRET),
            json={"content": message},
        )
        if response.status_code not in self.OK_STATUS_CODES:
            logger.error(
                "Webhook call failed: {}. Headers: {}.".format(
                    response.content, response.headers
                )
            )
            raise DiscordWebhookClientError(
                "Webhook call failed with code {}".format(response.status_code)
            )

    def send_message(self, message: str) -> None:
        self._request(message=message)
