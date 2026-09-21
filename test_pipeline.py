import sqlite3
import subprocess
import sys
from pathlib import Path

from src.pipeline import run_pipeline


def test_pipeline() -> None:
    run_pipeline()

    with sqlite3.connect("data/transactions.db") as connection:
        row_count = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        assert row_count == 15

        above_5000_count = connection.execute(
            "SELECT COUNT(*) FROM transactions WHERE above_5000 = 1"
        ).fetchone()[0]

        assert above_5000_count == 5

        total = connection.execute(
            """
            SELECT total_amount
            FROM sent_by_iban
            WHERE iban_origine = ?
            """,
            ("FR1111111111111111111111111",),
        ).fetchone()[0]

        assert float(total) == 10150.0

    run_pipeline()

    with sqlite3.connect("data/transactions.db") as connection:
        row_count_after_second_run = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        assert row_count_after_second_run == 15


def test_pipeline_failure() -> None:
    bad_file = Path("data/transactions_bad.csv")

    bad_file.write_text(
        "mauvais_colonne\n"
        "erreur\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "src.pipeline"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0

    with sqlite3.connect("data/transactions.db") as connection:
        row_count = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        assert row_count == 15

    bad_file.unlink()