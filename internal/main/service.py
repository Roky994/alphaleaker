import datetime
import logging
import time

from internal.core import db
from internal.main import messages
from internal.main.clients import apewisdom, discord

logger = logging.getLogger(__name__)


class TrendingCryptoCurrencies:
    TICKER_BLACKLIST = [
        "BTC",
        "ETH",
        "BNB",
        "SOL",
        "ADA",
        "XRP",
        "LUNA",
        "AVAX",
        "DOT",
        "USDC",
        "USDT",
        "PAX",
        "BUSD",
        "LINK",
        "LTC",
        "BCH",
    ]
    RANK_THRESHOLD = None
    MENTIONS_THRESHOLD = 50

    quiet = False

    def __init__(self, quiet=False) -> None:
        self.quiet = quiet

    def report(self) -> None:
        logger.info("Starting TrendingCryptoCurrencies report.")
        apewisdom_client = apewisdom.ApeWisdomClient()
        result = apewisdom_client.get_tredning_cryptocurrencies()

        for raw_ticker in result["results"]:
            trending_ticker = messages.TrendingTicker.from_api_dict(api_dict=raw_ticker)

            if (
                self.RANK_THRESHOLD is not None
                and trending_ticker.rank > self.RANK_THRESHOLD
            ):
                continue
            if (
                self.MENTIONS_THRESHOLD is not None
                and trending_ticker.mentions < self.MENTIONS_THRESHOLD
            ):
                continue

            self._handle_trending_ticker(trending_ticker)

    def _handle_trending_ticker(self, trending_ticker: messages.TrendingTicker) -> None:
        if trending_ticker.ticker in self.TICKER_BLACKLIST:
            return

        saved_trending_ticker = db.get_trending_ticker(ticker=trending_ticker.ticker)
        if saved_trending_ticker:
            if self._is_change_detected(trending_ticker, saved_trending_ticker):
                logger.info(
                    "Trending ticker {} with outdated data found, reporting.".format(
                        trending_ticker.ticker
                    )
                )
                self._save_and_report_ticker(trending_ticker=trending_ticker)
        else:
            logger.info(
                "New trending ticker {} found, reporting.".format(
                    trending_ticker.ticker
                )
            )
            self._save_and_report_ticker(trending_ticker=trending_ticker)

    def _is_change_detected(
        self,
        trending_ticker: messages.TrendingTicker,
        saved_trending_ticker: messages.TrendingTicker,
    ) -> bool:
        mentions_diff = (
            (trending_ticker.mentions / saved_trending_ticker.mentions) - 1
        ) * 100
        upvotes_diff = (
            (trending_ticker.upvotes / saved_trending_ticker.upvotes) - 1
        ) * 100

        if mentions_diff > 10 or upvotes_diff > 10:
            logger.info("Diff {} - {}".format(trending_ticker, saved_trending_ticker))
            return True

        return False

    def _save_and_report_ticker(self, trending_ticker: messages.TrendingTicker) -> None:
        if not self.quiet:
            discord.DiscordWebhookClient().send_message(
                message=self.get_alert_message(trending_ticker),
            )
            time.sleep(0.5)  # Rate limiting
        else:
            logger.info(
                "Skipping reporting ticker {} in quiet mode.".format(
                    trending_ticker.ticker
                )
            )

        db.insert_trending_ticker(trending_ticker=trending_ticker)

    def get_alert_message(self, trending_ticker: messages.TrendingTicker) -> str:
        rank_diff = ((trending_ticker.rank / trending_ticker.rank_24h_ago) - 1) * 100
        mentions_diff = (
            (trending_ticker.mentions / trending_ticker.mentions_24h_ago) - 1
        ) * 100

        message = (
            "\n"
            "\n**[{ticker}](https://apewisdom.io/cryptocurrencies/{ticker}/) ({name})**"
            "\n:triangular_flag_on_post: Rank: {rank} ({rank_diff}% last 24h)"
            "\n:speaking_head: Mentions: {mentions} ({mentions_diff}% last 24h)"
            "\n:point_up_2:  Upvotes: {upvotes}\n\n"
        ).format(
            ticker=trending_ticker.ticker,
            name=trending_ticker.name,
            rank=trending_ticker.rank,
            rank_diff="{}{:.0f}".format("+" if rank_diff > 0 else "", rank_diff),
            mentions=trending_ticker.mentions,
            mentions_diff="{}{:.0f}".format(
                "+" if mentions_diff > 0 else "", mentions_diff
            ),
            upvotes=trending_ticker.upvotes,
        )

        return message
