import hashlib
import sqlite3
from decimal import Decimal
from pathlib import Path

from src.database import create_database, insert_transactions
from src.generate import (
    DATA_DIR,
    TRANSACTIONS_1,
    TRANSACTIONS_2,
    TRANSACTIONS_3,
    write_csv,
)
from src.processing import (
    Transaction,
    load_csv,
    sum_by_destination_iban,
    sum_by_origin_iban,
    sum_by_source_bank,
)


DATABASE_PATH = DATA_DIR / "transactions.db"


def calculate_file_hash(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def is_file_already_processed(
    connection: sqlite3.Connection,
    content_hash: str,
) -> bool:
    result = connection.execute(
        "SELECT 1 FROM processed_files WHERE content_hash = ?",
        (content_hash,),
    ).fetchone()

    return result is not None


def mark_file_as_processed(
    connection: sqlite3.Connection,
    content_hash: str,
) -> None:
    connection.execute(
        "INSERT INTO processed_files (content_hash) VALUES (?)",
        (content_hash,),
    )


def update_sent_by_iban(
    connection: sqlite3.Connection,
    totals: dict[str, Decimal],
) -> None:
    for iban, total in totals.items():
        connection.execute(
            """
            INSERT INTO sent_by_iban (iban_origine, total_amount)
            VALUES (?, ?)
            ON CONFLICT(iban_origine)
            DO UPDATE SET total_amount =
                CAST(sent_by_iban.total_amount AS REAL)
                + CAST(? AS REAL)
            """,
            (iban, str(total), str(total)),
        )


def update_sent_by_bank(
    connection: sqlite3.Connection,
    totals: dict[str, Decimal],
) -> None:
    for bank, total in totals.items():
        connection.execute(
            """
            INSERT INTO sent_by_bank (banque_source, total_amount)
            VALUES (?, ?)
            ON CONFLICT(banque_source)
            DO UPDATE SET total_amount =
                CAST(sent_by_bank.total_amount AS REAL)
                + CAST(? AS REAL)
            """,
            (bank, str(total), str(total)),
        )


def update_received_by_iban(
    connection: sqlite3.Connection,
    totals: dict[str, Decimal],
) -> None:
    for iban, total in totals.items():
        connection.execute(
            """
            INSERT INTO received_by_iban (iban_destinataire, total_amount)
            VALUES (?, ?)
            ON CONFLICT(iban_destinataire)
            DO UPDATE SET total_amount =
                CAST(received_by_iban.total_amount AS REAL)
                + CAST(? AS REAL)
            """,
            (iban, str(total), str(total)),
        )


def insert_processing_results(
    connection: sqlite3.Connection,
    transactions: list[Transaction],
) -> None:
    update_sent_by_iban(
        connection,
        sum_by_origin_iban(transactions),
    )

    update_sent_by_bank(
        connection,
        sum_by_source_bank(transactions),
    )

    update_received_by_iban(
        connection,
        sum_by_destination_iban(transactions),
    )


def process_file(
    connection: sqlite3.Connection,
    file_path: Path,
) -> bool:
    content_hash = calculate_file_hash(file_path)

    if is_file_already_processed(connection, content_hash):
        return False

    transactions = load_csv(file_path)

    insert_transactions(connection, transactions)

    insert_processing_results(connection, transactions)

    mark_file_as_processed(connection, content_hash)

    connection.commit()

    return True


def generate_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    write_csv("transactions_1.csv", TRANSACTIONS_1)
    write_csv("transactions_2.csv", TRANSACTIONS_2)
    write_csv("transactions_3.csv", TRANSACTIONS_3)


def run_pipeline() -> None:
    generate_files()
    create_database(str(DATABASE_PATH))

    with sqlite3.connect(DATABASE_PATH) as connection:
        for file_path in sorted(DATA_DIR.glob("transactions_*.csv")):
            process_file(connection, file_path)


if __name__ == "__main__":
    run_pipeline()