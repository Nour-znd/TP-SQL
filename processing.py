import csv
from decimal import Decimal
from pathlib import Path
from typing import TypedDict


class Transaction(TypedDict):
    datetime_transaction: str
    iban_origine: str
    pays_source: str
    banque_source: str
    iban_destinataire: str
    pays_destinataire: str
    montant: Decimal
    devise: str
    above_5000: bool


def load_csv(file_path: Path) -> list[Transaction]:
    transactions: list[Transaction] = []

    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            transaction: Transaction = {
                "datetime_transaction": row["datetime_transaction"],
                "iban_origine": row["iban_origine"],
                "pays_source": row["pays_source"],
                "banque_source": row["banque_source"],
                "iban_destinataire": row["iban_destinataire"],
                "pays_destinataire": row["pays_destinataire"],
                "montant": Decimal(row["montant"]),
                "devise": row["devise"],
                "above_5000": Decimal(row["montant"]) > Decimal("5000"),
            }

            transactions.append(transaction)

    return transactions


def sum_by_origin_iban(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        iban = transaction["iban_origine"]
        amount = transaction["montant"]

        if iban not in totals:
            totals[iban] = Decimal("0")

        totals[iban] += amount

    return totals


def sum_by_source_bank(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        bank = transaction["banque_source"]
        amount = transaction["montant"]

        if bank not in totals:
            totals[bank] = Decimal("0")

        totals[bank] += amount

    return totals

def sum_by_destination_iban(
    transactions: list[Transaction],
) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}

    for transaction in transactions:
        iban = transaction["iban_destinataire"]
        amount = transaction["montant"]

        if iban not in totals:
            totals[iban] = Decimal("0")

        totals[iban] += amount

    return totals
    