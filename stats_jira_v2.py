from jiraone import LOGIN, PROJECT
from datetime import datetime


# L'action à réaliser pour extraire des données (1er filtre)
def what_action() -> str:
    global context
    print(context, "Que voulez-vous faire ? :")
    print(context, "     1 - Extraction des tickets")
    print(context, "     2 - Extraction de l'historique des tickets")
    choix = int(input('Choix [2] : ') or 2)
    if choix == 1:
        context.append("Tickets")
        return "tickets"
    else:
        context.append("Historique")
        return "histo"


# Sur quel pole on va réaliser l'action (2ème filtre)
def what_pole() -> str:
    global context
    print(context, "Pour quel pôle voulez-vous extraire les données ?", ' - '.join(poles))
    print(context, "ou pour un JQL personnalisé : [perso]")
    chosenPole: str = str(input('Pôle [perso] : ') or "perso")
    if chosenPole != "perso":
        print(context, "==> Extraction du pole", chosenPole, "...")
    else:
        print(context, "==> Extraction personnalisée...")

    context.append(chosenPole)
    return chosenPole


# Sur quelle période on sélectionne les données (3eme filtre)
def what_time(pole) -> int:
    global context
    if pole != "perso":
        print(context, "Sur quelle période ? :")
        print(context, "     1 - Le dernier jour")
        print(context, "     2 - Limité aux 2 dernières semaines")
        print(context, "     3 - Depuis le début des sprints")
        print(context, "     Autre - Personnalisée")
        choix = int(input('Choix [3] : ') or 3)
        return choix
    return 3


def defineJql(p, t) -> str:
    if p == "perso":
        persoJql = str(input('JQL personnalisé : '))
        return persoJql
    else:
        sprintIn = "Sprint in "
        projectDivalto = "project = DIVALTO AND "
        # Filtre sur les sprints du pole
        if p == 'SOE':
            filterIssues = sprintIn + "(" + ", ".join(map(str, sprintsSOE)) + ")"
            # Sprints 2 à 16 - SOE
        elif p == 'FIN':
            filterIssues = sprintIn + "(" + ", ".join(map(str, sprintsFIN)) + ")"
            # Sprints 1 à 7 - Finance
        elif p == 'SOI':
            filterIssues = sprintIn + "(" + ", ".join(map(str, sprintsSOI)) + ")"
            # Sprints SOI-Eu
        elif p == 'SOPCA':
            filterIssues = sprintIn + "(" + ", ".join(map(str, sprintsSOPCA)) + ")"
            # Sprints SopCa
        elif p == 'INFRA':
            filterIssues = "labels = DIVALTO_INFRA AND statusCategory not in (Done)"
        elif p == 'R&D':
            # not working
            filterIssues = "((text \~ \"R&D\" OR text \~ \"agil?o\") AND (text \~ Ticket OR text \~ Demande) OR text \~ \"EDITEUR/STANDARD\") AND status not in (CLOSED, Done, Fermé, Cancelled, \"Ready for UAT\", \"UAT\") "
        else:
            filterIssues = ""

        # Filtre sur la période
        if t == 1:
            time = " AND (updated > -1d OR updatedDate > -1d)"
        elif t == 2:
            time = " AND (updated > -14d OR updatedDate > -14d)"
        elif t == 3:
            time = ""
        else:
            jours = int(input('Depuis combien de jours ? [15] : ') or 15)
            time = " AND (updated > -" + str(jours) + "d OR updatedDate > -" + str(jours) + "d)"

        jql = projectDivalto + filterIssues + time
    return jql


# Tickets
def exportIssues(p):
    text = [dateCourante, str(p), "Tickets"]
    fileName = '_'.join(text) + extension  # Fichier de sortie des données des tickets
    print(fileName)
    PROJECT.export_issues(jql=jql, folder=destinationFolder, final_file=fileName)


# Historique des tickets
def exportHistorique(p):
    text = [dateCourante, str(p), "Historique"]
    fileNameHisto = '_'.join(text)  # Fichier de sortie des données de l'historique des tickets
    PROJECT.change_log(jql=jql, folder=destinationFolder, file=fileNameHisto + extension)


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
    context = []

    # Liste des pôles
    poles = ['SOI', 'SOE', 'FIN', 'SOPCA', 'INFRA', 'R&D']
    # Et leur sprints actuels
    sprintsSOE = [255, 257, 258, 265, 267, 272, 273, 282, 290, 292, 295, 296, 297, 305, 319]
    sprintsSOI = [262, 263, 266, 271, 274, 281, 289, 291, 299, 306, 307, 317, 321, 324]
    sprintsFIN = [275, 277, 283, 298, 304, 320, 325]
    sprintsSOPCA = [293, 300, 308, 310, 318, 322, 330]

    # Date courante avec heure
    dateCourante = datetime.now().strftime("%d-%m-%YT%H-%M-%S")

    # Show "logo"
    print("=====================================================================================================")
    print("                                     ", "Divalto JIRA", "                                         ")
    print("=====================================================================================================")
    print("Date :", dateCourante)

    # Changement de la structure d'appel - v0.2
    action = what_action()
    pole = what_pole()
    time = what_time(pole)
    jql = defineJql(pole, time)
    print(context, "JQL : ", jql)
    match action:
        case "tickets":
            exportIssues(pole)
        case "histo":
            exportHistorique(pole)
