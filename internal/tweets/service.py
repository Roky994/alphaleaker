import datetime
import logging
import os
import time

from dotenv import load_dotenv

from internal.common.clients import twitter
from internal.common.clients import discord

logger = logging.getLogger(__name__)


class TweetsService:
    discord_client = None

    USERS = {
        784068635958644736: "cryptodetweiler",
        37839293: "Tetranode",
        905395394: "AndreCronjeTech",
        1214090353826942976: "chng_raymond",
        1383844736260210691: "shitc0in",
        1480297433020215297: "thedefiedge",
    }
    RECENT_TWEETS_IN_MINUTES = 15  # Match interval for running

    def __init__(self) -> None:
        load_dotenv()

    def report(self) -> None:
        logger.info("Starting Sniper report.")

        self.discord_client = discord.DiscordWebhookClient(
            webhook_secret=os.getenv("DISCORD_WH_SECRET_TWEETS")
        )

        twitter_client = twitter.TwitterClient()
        for user_id, username in self.USERS.items():
            result = twitter_client.get_user_tweets(
                user_id=user_id,
                datetime_from=datetime.datetime.now()
                - datetime.timedelta(minutes=self.RECENT_TWEETS_IN_MINUTES),
            )
            for tweet in result.get("data", []):
                tweet_text = tweet["text"]
                if "$" in tweet_text or "http" in tweet_text or "@" in tweet_text:
                    msg = "https://twitter.com/{}:\n{}".format(username, tweet_text)
                    print(msg)
                    print()

                self.discord_client.send_message(
                    message=msg,
                )
                time.sleep(0.5)  # Rate limiting
