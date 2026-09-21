import sqlite3
import time
from collections.abc import Callable, Iterable
from decimal import Decimal
from typing import Any

from src.processing import Transaction


def create_database(database_path: str) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime_transaction TEXT NOT NULL,
                iban_origine TEXT NOT NULL,
                pays_source TEXT NOT NULL,
                banque_source TEXT NOT NULL,
                iban_destinataire TEXT NOT NULL,
                pays_destinataire TEXT NOT NULL,
                montant TEXT NOT NULL,
                devise TEXT NOT NULL,
                above_5000 INTEGER NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS sent_by_iban (
                iban_origine TEXT PRIMARY KEY,
                total_amount TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS sent_by_bank (
                banque_source TEXT PRIMARY KEY,
                total_amount TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS received_by_iban (
                iban_destinataire TEXT PRIMARY KEY,
                total_amount TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                content_hash TEXT PRIMARY KEY
            )
        """)


def execute_with_retry(
    operation: Callable[[], sqlite3.Cursor],
    max_retries: int = 3,
    delay_seconds: float = 0.1,
) -> sqlite3.Cursor:
    for attempt in range(max_retries):
        try:
            return operation()
        except sqlite3.OperationalError as error:
            message = str(error).lower()

            if "locked" not in message and "busy" not in message:
                raise

            if attempt == max_retries - 1:
                raise

            time.sleep(delay_seconds)

    raise RuntimeError("Le retry n'a pas pu aboutir")


def insert_transactions(
    connection: sqlite3.Connection,
    transactions: Iterable[Transaction],
) -> None:
    for transaction in transactions:

        def insert() -> sqlite3.Cursor:
            return connection.execute(
                """
                INSERT INTO transactions (
                    datetime_transaction,
                    iban_origine,
                    pays_source,
                    banque_source,
                    iban_destinataire,
                    pays_destinataire,
                    montant,
                    devise,
                    above_5000
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction["datetime_transaction"],
                    transaction["iban_origine"],
                    transaction["pays_source"],
                    transaction["banque_source"],
                    transaction["iban_destinataire"],
                    transaction["pays_destinataire"],
                    str(transaction["montant"]),
                    transaction["devise"],
                    int(transaction["above_5000"]),
                ),
            )

        execute_with_retry(insert)
from unittest.mock import Mock

from src.database import execute_with_retry


def test_retry_on_locked_database() -> None:
    operation = Mock(
        side_effect=[
            sqlite3.OperationalError("database is locked"),
            sqlite3.connect(":memory:").execute("SELECT 1"),
        ]
    )

    result = execute_with_retry(
        operation,
        max_retries=3,
        delay_seconds=0,
    )

    assert result is not None
    assert operation.call_count == 2