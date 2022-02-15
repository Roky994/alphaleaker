import datetime
import logging
import os
import time

from dotenv import load_dotenv

from internal.common.clients import twitter
from internal.common.clients import discord

logger = logging.getLogger(__name__)


class SniperService:
    discord_client = None

    USERNAME_KEYWORDS = {"protocol", "defi" "decentralised "}

    def __init__(self) -> None:
        load_dotenv()

    def report(self) -> None:
        logger.info("Starting Sniper report.")

        self.discord_client = discord.DiscordWebhookClient(
            webhook_secret=os.getenv("DISCORD_WH_SECRET_TWEETS")
        )

        twitter_client = twitter.TwitterClient()

        # Criteria
        # Created at < last 14 days

        result = twitter_client.search_users()
        print(result)
