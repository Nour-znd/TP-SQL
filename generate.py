import csv
from pathlib import Path


DATA_DIR = Path("data")


TRANSACTIONS_1 = [
    [
        "2024-03-01T09:12:00",
        "FR1111111111111111111111111",
        "FR",
        "BNPPARIBAS",
        "DE2222222222222222222222",
        "DE",
        "1200.00",
        "EUR",
    ],
    [
        "2024-03-01T10:45:00",
        "FR3333333333333333333333333",
        "FR",
        "CREDITAGRICOLE",
        "ES3333333333333333333333",
        "ES",
        "7500.00",
        "EUR",
    ],
    [
        "2024-03-01T11:30:00",
        "FR1111111111111111111111111",
        "FR",
        "BNPPARIBAS",
        "IT4444444444444444444444",
        "IT",
        "300.00",
        "EUR",
    ],
    [
        "2024-03-01T13:20:00",
        "FR6666666666666666666666666",
        "FR",
        "SOCIETEGENERALE",
        "DE2222222222222222222222",
        "DE",
        "6200.00",
        "EUR",
    ],
    [
        "2024-03-01T15:10:00",
        "FR3333333333333333333333333",
        "FR",
        "CREDITAGRICOLE",
        "ES5555555555555555555555",
        "ES",
        "900.00",
        "EUR",
    ],
]


TRANSACTIONS_2 = [
    [
        "2024-03-02T09:00:00",
        "FR1111111111111111111111111",
        "FR",
        "BNPPARIBAS",
        "DE6666666666666666666666",
        "DE",
        "2500.00",
        "EUR",
    ],
    [
        "2024-03-02T10:15:00",
        "FR3333333333333333333333333",
        "FR",
        "CREDITAGRICOLE",
        "ES7777777777777777777777",
        "ES",
        "6000.00",
        "EUR",
    ],
    [
        "2024-03-02T12:40:00",
        "FR4444444444444444444444444",
        "FR",
        "BNPPARIBAS",
        "FR1111111111111111111111111",
        "FR",
        "450.00",
        "EUR",
    ],
    [
        "2024-03-02T14:30:00",
        "FR5555555555555555555555555",
        "FR",
        "SOCIETEGENERALE",
        "DE2222222222222222222222",
        "DE",
        "1800.00",
        "EUR",
    ],
    [
        "2024-03-02T16:00:00",
        "FR3333333333333333333333333",
        "FR",
        "CREDITAGRICOLE",
        "FR6666666666666666666666666",
        "FR",
        "700.00",
        "EUR",
    ],
]


TRANSACTIONS_3 = [
    [
        "2024-03-03T08:45:00",
        "FR1111111111111111111111111",
        "FR",
        "BNPPARIBAS",
        "FR3333333333333333333333333",
        "FR",
        "5500.00",
        "EUR",
    ],
    [
        "2024-03-03T10:20:00",
        "FR7777777777777777777777777",
        "FR",
        "SOCIETEGENERALE",
        "DE4444444444444444444444",
        "DE",
        "800.00",
        "EUR",
    ],
    [
        "2024-03-03T12:15:00",
        "FR3333333333333333333333333",
        "FR",
        "CREDITAGRICOLE",
        "DE6666666666666666666666",
        "DE",
        "3200.00",
        "EUR",
    ],
    [
        "2024-03-03T14:50:00",
        "FR1111111111111111111111111",
        "FR",
        "BNPPARIBAS",
        "ES5555555555555555555555",
        "ES",
        "650.00",
        "EUR",
    ],
    [
        "2024-03-03T16:30:00",
        "FR9999999999999999999999999",
        "FR",
        "BNPPARIBAS",
        "FR2222222222222222222222222",
        "FR",
        "9000.00",
        "EUR",
    ],
]


def create_data_directory() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def write_csv(filename: str, transactions: list[list[str]]) -> None:
    file_path = DATA_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "datetime_transaction",
            "iban_origine",
            "pays_source",
            "banque_source",
            "iban_destinataire",
            "pays_destinataire",
            "montant",
            "devise",
        ])

        writer.writerows(transactions)


def main() -> None:
    create_data_directory()

    write_csv("transactions_1.csv", TRANSACTIONS_1)
    write_csv("transactions_2.csv", TRANSACTIONS_2)
    write_csv("transactions_3.csv", TRANSACTIONS_3)


if __name__ == "__main__":
    main()