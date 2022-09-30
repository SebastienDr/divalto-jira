# divalto-jira
Extract de données de JIRA pour Divalto
Use stats_jira_v2.py.

v0.3 (Actual)

Requirements : 
--------------
- Python >= 3.6
- [JiraOne](https://pypi.org/project/jiraone/ "jiraone") installé

Usage :
-------

1. Taper `python stats_jira_v2.py` dans la console
2. Suivez les instructions à l'écran
3. Actuellement les fichiers se retrouvent à la racine dans le répertoire \Divalto
    - Il y a 2 types de fichiers .txt : un pour l'historique et un pour les tickets
    - Ils sont tous les 2 au format CSV (pour des soucis d'encodings, il faut pour le moment les importer à la main dans Excel)
4. Ouvrir Excel
5. Onglet Données > Ouvrir des données > Importer à partir d'un fichier
6. Choisir l'un des fichiers > Cliquer sur Charger
7. Vos données sont importées !

Note :
------
- Il faut modifier le reporting.py par défaut de Jiraone car il ne gère pas l'encoding de Windows correctement 
(ou alors je n'ai pas encore compris comment lui forcer un encoding particulier)
