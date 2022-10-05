Changelog

Les changements au programme seront reportés (manuellement pour l'instant) dans ce fichier.

v0.1

    27 Sep 2022

    note: project initialization
    params: added the 5 Divalto entities
    feat: added jiraone change_log for issues history 
    feat: added jiraone export_issues for issues content
    note: all entities have their dedicated files for _History and _Issues in Divalto directory
    feat: added ALL option to generate files for ALL Divalto entities

v0.2

    29 Sep 2022
    note : refactoring of interface display
    feat: added segmentation for action/pole and period
    feat: added R&D pole
    knownbug : R&D jql is not working properly because of special characters ~ not parsed correctly
    note: removed ALL option as it did not seem relevant
    note: refactoring of interface => less hardcoded stuff

v0.3

    29 Sep 2022
    knownbug: if 0 issues are found through jql, program crashes
    feat: added choose sprint option
    note: removed R&D pole
    feat: added timestamp to files extracts

v0.4

    05 Oct 2022
    feat: externalized properties. You can now connect to your own JIRA with your credentials
    note: code cleaned a bit to respect python code style
