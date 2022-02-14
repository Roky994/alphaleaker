import logging

import requests

logger = logging.getLogger(__name__)


class DiscordWebhookClientError(Exception):
    pass


class DiscordWebhookClient:
    _webhook_secret = None

    BASE_DISCORD_URL = "https://discord.com/api/webhooks"
    OK_STATUS_CODES = [204]

    def __init__(self, webhook_secret: str) -> None:
        self._webhook_secret = webhook_secret

    def _request(self, message: str) -> None:
        response = requests.post(
            "{}/{}".format(self.BASE_DISCORD_URL, self._webhook_secret),
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
