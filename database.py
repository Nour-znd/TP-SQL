import sqlite3
from decimal import Decimal
from typing import Iterable

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


def insert_transactions(
    database_path: str,
    transactions: Iterable[Transaction],
) -> None:
    with sqlite3.connect(database_path) as connection:
        for transaction in transactions:
            connection.execute(
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