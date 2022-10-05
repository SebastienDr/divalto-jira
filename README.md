# divalto-jira
Extract de données de JIRA pour Divalto. Use stats_jira.py.

**v0.3 (Actual)**

Requirements : 
--------------
- Python >= 3.6
- [JiraOne](https://pypi.org/project/jiraone/ "jiraone") installé

Usage :
-------

1. (Facultatif) Editer le fichier `stats_jira.yaml` avec un bloc-notes pour définir la connexion à JIRA ou la
destination des fichiers générés
2. Taper `python stats_jira.py` dans la console ou lancez le `stats_jira.exe` à la racine du répertoire d'installation
3. Suivez les instructions à l'écran
4. Actuellement les fichiers se retrouvent à la racine dans le répertoire \Divalto
    - Il y a 2 types de fichiers .txt : un pour l'historique et un pour les tickets
    - Ils sont tous les 2 au format CSV (pour des soucis d'encodings, il faut pour le moment les importer à la main dans Excel)
5. Ouvrir Excel
6. Onglet Données > Ouvrir des données > Importer à partir d'un fichier
7. Choisir l'un des fichiers > Cliquer sur Charger
8. Vos données sont importées !


Note :
------
Etapes d'installation (à automatiser si possible) :
- Installer python >= 3.6
- Installer jiraone
- Modifier le reporting.py par défaut de Jiraone car il ne gère pas l'encoding de Windows correctement 
(ou alors je n'ai pas encore compris comment lui forcer un encoding particulier)


Idées pour les futures releases :
---------------------------------
- Tester la librairie panda pour la gestion des CSV et Excel
- Automatiser la création d'un exe et fournir une commande complète pour le créer à partir du source code