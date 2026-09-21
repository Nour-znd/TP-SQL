Étape 6 — Gestion des erreurs
Échec du pipeline

Un fichier CSV volontairement incorrect a été utilisé afin de provoquer une erreur lors du traitement.

Le test vérifie que le pipeline retourne un code de retour différent de 0 et qu'aucune insertion partielle n'est effectuée dans la base de données.

Commande utilisée :

python -m pytest -s tests/test_pipeline.py::test_pipeline_failure

Résultat du test :

1 passed

Erreur détectée uniquement par mypy

Une erreur de typage volontaire a été ajoutée dans src/processing.py :

nombre: int = "bonjour"

Mypy a détecté l'erreur suivante :

src\processing.py:77: error: Incompatible types in assignment (expression has type "str", variable has type "int") [assignment]
Found 1 error in 1 file (checked 7 source files)

Cette erreur n'est pas détectée par pytest car elle concerne le typage statique du code. Mypy vérifie la cohérence des types, tandis que pytest vérifie le comportement du programme lors de son exécution.

Après suppression de l'erreur volontaire, mypy retourne :

Success: no issues found in 7 source files

### Retry des erreurs SQLite

Une erreur `sqlite3.OperationalError` peut être temporaire, notamment lorsque la base de données est verrouillée. Dans ce cas, une nouvelle tentative peut réussir après un court délai.

À l'inverse, une erreur `sqlite3.IntegrityError` correspond à une violation d'une contrainte de la base de données. Réessayer la même opération ne permet pas de corriger cette erreur.

Le mécanisme de retry a donc été implémenté uniquement pour les erreurs `OperationalError` liées à une base verrouillée ou occupée (`locked` ou `busy`).

Le retry effectue jusqu'à 3 tentatives avec un court délai entre les tentatives.

Un test simule une erreur `database is locked` lors de la première tentative puis vérifie que la deuxième tentative réussit.

Commande utilisée :

python -m pytest

Résultat :

5 passed