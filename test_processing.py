from decimal import Decimal

from src.processing import (
    Transaction,
    sum_by_destination_iban,
    sum_by_origin_iban,
    sum_by_source_bank,
)


def make_transactions() -> list[Transaction]:
    return [
        {
            "datetime_transaction": "2024-03-01T10:00:00",
            "iban_origine": "FR111",
            "pays_source": "FR",
            "banque_source": "BNP",
            "iban_destinataire": "DE111",
            "pays_destinataire": "DE",
            "montant": Decimal("1000"),
            "devise": "EUR",
            "above_5000": False,
        },
        {
            "datetime_transaction": "2024-03-01T11:00:00",
            "iban_origine": "FR111",
            "pays_source": "FR",
            "banque_source": "BNP",
            "iban_destinataire": "DE222",
            "pays_destinataire": "DE",
            "montant": Decimal("6000"),
            "devise": "EUR",
            "above_5000": True,
        },
        {
            "datetime_transaction": "2024-03-01T12:00:00",
            "iban_origine": "FR222",
            "pays_source": "FR",
            "banque_source": "CA",
            "iban_destinataire": "DE111",
            "pays_destinataire": "DE",
            "montant": Decimal("2000"),
            "devise": "EUR",
            "above_5000": False,
        },
    ]


def test_sum_by_origin_iban() -> None:
    transactions = make_transactions()

    result = sum_by_origin_iban(transactions)

    assert result["FR111"] == Decimal("7000")
    assert result["FR222"] == Decimal("2000")


def test_sum_by_source_bank() -> None:
    transactions = make_transactions()

    result = sum_by_source_bank(transactions)

    assert result["BNP"] == Decimal("7000")
    assert result["CA"] == Decimal("2000")


def test_sum_by_destination_iban() -> None:
    transactions = make_transactions()

    result = sum_by_destination_iban(transactions)

    assert result["DE111"] == Decimal("3000")
    assert result["DE222"] == Decimal("6000")