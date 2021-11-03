import datetime
import typing


class TrendingTicker(typing.NamedTuple):
    ticker: str
    name: str
    rank: int
    mentions: int
    upvotes: int
    rank_24h_ago: int
    mentions_24h_ago: int
    created_at: datetime.datetime

    @classmethod
    def from_api_dict(cls, api_dict: dict):
        return cls(
            ticker=api_dict["ticker"].replace(".X", ""),
            name=api_dict["name"],
            rank=int(api_dict["rank"]),
            mentions=int(api_dict["mentions"]),
            upvotes=int(api_dict["upvotes"]),
            rank_24h_ago=int(api_dict["rank_24h_ago"])
            if api_dict["rank_24h_ago"]
            else 0,
            mentions_24h_ago=int(api_dict["mentions_24h_ago"])
            if api_dict["mentions_24h_ago"]
            else 0,
            created_at=datetime.datetime.now(),
        )

    @classmethod
    def from_db(cls, db_row: dict):
        if not db_row:
            return None

        return cls(
            ticker=db_row[0],
            name=db_row[1],
            rank=int(db_row[2]),
            mentions=int(db_row[3]),
            upvotes=int(db_row[4]),
            rank_24h_ago=int(db_row[5]),
            mentions_24h_ago=int(db_row[6]),
            created_at=datetime.datetime.strptime(db_row[7], "%Y-%m-%d %H:%M:%S"),
        )
