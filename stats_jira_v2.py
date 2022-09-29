from jiraone import LOGIN, PROJECT


def what_pole() -> str:
    global context
    print(context + "Pour quel pôle voulez-vous extraire les données ? ", list(poles.keys()))
    print(context + "ou pour un JQL personnalisé : [perso] ")
    chosenPole: str = str(input('Pôle [perso] : ') or "perso")
    print("")
    context += "[" + chosenPole + "] "
    if chosenPole != "perso":
        print("====================================", poles.get(chosenPole), "====================================")
    else:
        print("===================================================================================================")
        print(context + action, "==> Extraction personnalisée...")

    print("")
    return chosenPole


def what_action() -> str:
    global context
    print("===========================================", "Divalto JIRA", "===========================================")
    print("Que voulez-vous faire ? :")
    print("     1 - Extraction des tickets")
    print("     2 - Extraction de l'historique des tickets")
    choix = int(input('Choix [2] : ') or 2)
    print("")
    if choix == 1:
        context = "(Tickets) "
        return "tickets"
    else:
        context = "(Historique) "
        return "histo"


def jqlPerso() -> str:
    persoJql = str(input('JQL personnalisé : '))
    return persoJql


def defineJql(p, t) -> str:
    if p == "perso":
        jql = jqlPerso()
    else:
        sprintIn = "Sprint in ("
        projectDivalto = "project = DIVALTO AND "
        if p == 'SOE':
            filterIssues = sprintIn + "255, 257, 258, 265, 267, 272, 273, 282, 290, 292, 295, 296, 297, 305, 319)"
            # Sprints 2 à 16 - SOE
        elif p == 'FIN':
            filterIssues = sprintIn + "275, 277, 283, 298, 304, 320, 325)"
            # Sprints 1 à 7 - Finance
        elif p == 'SOI':
            filterIssues = sprintIn + "262, 263, 266, 271, 274, 281, 289, 291, 299, 306, 307, 317, 321, 324)"
            # Sprints SOI-Eu
        elif p == 'SOPCA':
            filterIssues = sprintIn + "293, 300, 308, 310, 318, 322, 330)"
            # Sprints SopCa
        elif p == 'INFRA':
            filterIssues = "labels = DIVALTO_INFRA AND statusCategory not in (Done)"
        elif p == 'R&D':
            filterIssues = "((text ~ 'R&D' OR text ~ 'agil?o') AND (text ~ Ticket OR text ~ Demande) OR text ~ 'EDITEUR/STANDARD') AND status not in (CLOSED, Done, Fermé, Cancelled, 'Ready for UAT','UAT') "
        else:
            filterIssues = ""

        if t == 1:
            time = " AND (updated > -1d OR updatedDate > -1d)"
        elif t == 2:
            time = " AND (updated > -14d OR updatedDate > -14d)"
        else:
            time = ""
        jql = projectDivalto + filterIssues + time
    return jql


def what_time(pole) -> int:
    global context
    if pole != "perso":
        print(context + "=> Sur quelle période ? :")
        print(context + "     1 - Le dernier jour")
        print(context + "     2 - Limité aux 2 dernières semaines")
        print(context + "     3 - Depuis le début des sprints")
        print(context + "     4 - Personnalisée")
        choix = int(input('Choix [3] : ') or 3)
        return choix
    return 3


def exportIssues(p):
    fileName = str(p) + "_Tickets"  # Fichier de sortie des données des tickets
    # Tickets
    PROJECT.export_issues(jql=jql, folder=destinationFolder, final_file=fileName + extension)


def exportHistorique(p):
    fileNameHisto = str(p) + "_Historique"  # Fichier de sortie des données de l'historique des tickets
    # Historique des tickets
    PROJECT.change_log(folder=destinationFolder, file=fileNameHisto + extension, jql=jql)


# Programme principal
if __name__ == "__main__":

    # Connexion à JIRA
    user = "sdrouard.ext"
    password = "SOP1_Avecesar1"
    link = "https://jira.soprema.ca"
    LOGIN.api = False  # comment out line, if you want to extract history from a cloud instance
    LOGIN(user=user, password=password, url=link)

    # Gestion des fichiers
    destinationFolder = "Divalto"
    extension = ".txt"  # Pour le moment : pour éviter les problèmes d'encoding
    context = "= "

    # Liste des pôles
    poles = {'SOI': 'SOI', 'SOE': 'SOE', 'FIN': 'Finance', 'SOPCA': 'SopCa', 'INFRA': 'Infra', 'R&D': 'R&D'}

    # Changement de la structure d'appel - v0.2
    action = what_action()
    pole = what_pole()
    time = what_time(pole)
    jql = defineJql(pole, time)
    print(context + "JQL : ", jql)
    match action:
        case "tickets":
            exportIssues(pole)
        case "histo":
            exportHistorique(pole)
