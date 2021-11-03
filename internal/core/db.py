import os
import sqlite3
import typing

from dotenv import load_dotenv
from internal.main import messages

load_dotenv()
DB_PATH = os.getenv("DB_PATH")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def migrate(drop: bool = False) -> None:
    con = get_connection()
    cur = con.cursor()

    if drop:
        cur.execute("DROP TABLE trending_ticker;")

    cur.execute(
        """
        CREATE TABLE trending_ticker (
            id INT PRIMARY KEY,
            ticker TEXT NOT NULL,
            name TEXT NOT NULL,
            rank INT NOT NULL,
            mentions INT NOT NULL,
            upvotes INT NOT NULL,
            rank_24h_ago INT NOT NULL,
            mentions_24h_ago INT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    con.commit()
    con.close()


def insert_trending_ticker(trending_ticker: messages.TrendingTicker) -> int:
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO trending_ticker (
            ticker,
            name,
            rank,
            mentions,
            upvotes,
            rank_24h_ago,
            mentions_24h_ago,
            created_at
        ) VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            datetime('now')
        );
        """,
        [
            trending_ticker.ticker,
            trending_ticker.name,
            trending_ticker.rank,
            trending_ticker.mentions,
            trending_ticker.upvotes,
            trending_ticker.rank_24h_ago,
            trending_ticker.mentions_24h_ago,
        ],
    )
    con.commit()
    id = cur.lastrowid

    con.close()

    return id


def get_trending_ticker(ticker: str) -> typing.Optional[messages.TrendingTicker]:
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        SELECT 
            ticker, 
            name, 
            rank,
            mentions,
            upvotes, 
            rank_24h_ago,
            mentions_24h_ago, 
            created_at 
        FROM trending_ticker
        WHERE ticker = ?
        ORDER BY created_at DESC 
        LIMIT 1;
        """,
        [ticker],
    )
    record = cur.fetchone()
    con.close()

    return messages.TrendingTicker.from_db(record)
