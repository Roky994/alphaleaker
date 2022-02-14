import os
import sqlite3

from dotenv import load_dotenv

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
