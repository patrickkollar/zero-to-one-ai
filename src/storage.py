"""
Persistence layer.

The memory layer decides what the system knows.
The storage layer makes that knowledge survive between runs.

This reference implementation uses SQLite because it is:
- local
- lightweight
- easy to inspect
- sufficient for a single-user prototype
"""

import sqlite3
from pathlib import Path


class Storage:
    def __init__(self, database_path: str = "data/job_needle_finder.db"):
        self.database_path = database_path

        Path(database_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(database_path)

        self._initialize()

    def _initialize(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                preference TEXT NOT NULL UNIQUE
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS exclusions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exclusion TEXT NOT NULL UNIQUE
            )
            """
        )

        self.connection.commit()

    def save_decision(
        self,
        job_id: str,
        decision: str,
        reason: str,
    ):
        self.connection.execute(
            """
            INSERT INTO decisions (
                job_id,
                decision,
                reason
            )
            VALUES (?, ?, ?)
            """,
            (job_id, decision, reason),
        )

        self.connection.commit()

    def get_decisions(self):
        cursor = self.connection.execute(
            """
            SELECT job_id, decision, reason
            FROM decisions
            """
        )

        return cursor.fetchall()

    def save_preference(self, preference: str):
        self.connection.execute(
            """
            INSERT OR IGNORE INTO preferences (preference)
            VALUES (?)
            """,
            (preference,),
        )

        self.connection.commit()

    def save_exclusion(self, exclusion: str):
        self.connection.execute(
            """
            INSERT OR IGNORE INTO exclusions (exclusion)
            VALUES (?)
            """,
            (exclusion,),
        )

        self.connection.commit()
