from jiraone import LOGIN, PROJECT
from datetime import datetime
import yaml


# L'action à réaliser pour extraire des données (1er filtre)
def what_action() -> str:
    global context
    print(context, "Que voulez-vous faire ? :")
    print(context, "1 - Extraction des tickets".rjust(5))
    print(context, "2 - Extraction de l'historique des tickets".rjust(5))
    print(context, "3 - Quitter".rjust(5))
    choix = int(input('Choix [2] : ') or 2)
    if choix == 1:
        print("=====> Extraction des tickets")
        context.append("Tickets")
        return "tickets"
    elif choix == 2:
        print("=====> Extraction de l'historique")
        context.append("Historique")
        return "histo"
    else:
        print("=====> Au revoir !")
        return "quit"


# Sur quel pole on va réaliser l'action (2ème filtre)
def what_pole() -> str:
    global context
    print(context, "Pour quel pôle voulez-vous extraire les données ?", " - ".join(poles))
    print(context, "ou alors un JQL personnalisé : [perso]")
    chosen_pole: str = str(input('Pôle [perso] : ') or "perso")
    if chosen_pole != "perso":
        print("=====> Sur le pole", chosen_pole, "...")
    else:
        print("=====> Via un JQL personnalisé...")

    context.append(chosen_pole)
    return chosen_pole


# Sur quels sprints on sélectionne les données (3eme filtre)
def what_sprint() -> str:
    global context, sprints
    print(context, "Sur quel(s) sprint(s) ? :")
    print(context, "1 - Tous".rjust(5))
    print(context, "2 - Personnalisés - en liste séparé par des ',' (Ex : 215,217,233) -".rjust(5))
    sprints = str(input('Choix [Tous] : ') or "Tous")
    print("=====> Extraction des sprints :", sprints)
    context.append(sprints)

    return sprints


# Sur quelle période on sélectionne les données (4eme filtre)
def what_time(p) -> int:
    global context
    if p != "perso":
        print(context, "Sur quelle période ? :")
        print(context, "1 - Le dernier jour".rjust(5))
        print(context, "2 - Limité aux 2 dernières semaines".rjust(5))
        print(context, "3 - Depuis le début des sprints".rjust(5))
        print(context, "Autre - Personnalisée".rjust(5))
        choix = int(input('Choix [3] : ') or 3)
        return choix
    return 3


def define_jql() -> str:
    if pole == "perso":
        return str(input("JQL personnalisé : "))
    else:
        sprint_in = "Sprint in "
        project_divalto = "project = DIVALTO AND "

        # Filtre sur les poles
        match pole:
            case 'SOE':
                if sprints == "Tous":
                    filter_issues = sprint_in + "(" + ", ".join(map(str, sprintsSOE)) + ")"
                else:
                    filter_issues = sprint_in + "(" + sprints + ")"
            case 'FIN':
                if sprints == "Tous":
                    filter_issues = sprint_in + "(" + ", ".join(map(str, sprintsFIN)) + ")"
                else:
                    filter_issues = sprint_in + "(" + sprints + ")"
            case 'SOI':
                if sprints == "Tous":
                    filter_issues = sprint_in + "(" + ", ".join(map(str, sprintsSOI)) + ")"
                else:
                    filter_issues = sprint_in + "(" + sprints + ")"
            case 'SOPCA':
                if sprints == "Tous":
                    filter_issues = sprint_in + "(" + ", ".join(map(str, sprintsSOPCA)) + ")"
                else:
                    filter_issues = sprint_in + "(" + sprints + ")"
            case 'INFRA':
                filter_issues = "labels = DIVALTO_INFRA AND statusCategory not in (Done)"
            case _:
                filter_issues = ""

        # Filtre sur la période
        if time == 1:
            time_str = " AND (updated > -1d OR updatedDate > -1d)"
        elif time == 2:
            time_str = " AND (updated > -14d OR updatedDate > -14d)"
        elif time == 3:
            time_str = ""
        else:
            jours = int(input('Depuis combien de jours ? [15] : ') or 15)
            time_str = " AND (updated > -" + str(jours) + "d OR updatedDate > -" + str(jours) + "d)"

        future_jql = project_divalto + filter_issues + time_str
    return future_jql


# Tickets
def export_issues(p):
    text = [dateCourante, str(p), "Tickets"]
    file_name = '_'.join(text) + extension  # Fichier de sortie des données des tickets
    print(file_name)
    PROJECT.export_issues(jql=jql, folder=destinationFolder, final_file=file_name)


# Historique des tickets
def export_historique(p):
    text = [dateCourante, str(p), "Historique"]
    file_name_histo = '_'.join(text)  # Fichier de sortie des données de l'historique des tickets
    PROJECT.change_log(jql=jql, folder=destinationFolder, file=file_name_histo + extension)


# Programme principal
if __name__ == "__main__":

    with open(r'properties/stats_jira.yaml', encoding='utf8') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        # Chargement des propriétés du programme
        props = yaml.load(file, Loader=yaml.FullLoader)

    # Connexion à JIRA Instance
    LOGIN.api = False  # comment out line, if you want to extract history from a cloud instance
    LOGIN(user=props.get('jira.user'), password=props.get('jira.password'), url=props.get('jira.link'))

    # Gestion des fichiers
    destinationFolder = props.get('destination.folder')
    extension = ".txt"  # Pour le moment : pour éviter les problèmes d'encoding
    context = []

    # Liste des pôles
    poles = props.get('divalto.poles')
    # Et leurs sprints actuels
    sprintsSOE = props.get('soe.sprints')
    sprintsSOI = props.get('soi.sprints')
    sprintsFIN = props.get('fin.sprints')
    sprintsSOPCA = props.get('sopca.sprints')

    # Date courante avec heure
    dateCourante = datetime.now().strftime("%d-%m-%YT%H-%M-%S")

    # Show "logo"
    print("=====================================================================================================")
    print("                                     ", "Divalto JIRA", "                                         ")
    print("=====================================================================================================")
    dateShown = dateCourante.split('T')
    print("Date :", "Le", dateShown.pop(0), "à", dateShown.pop())
    if props.get('show.properties'):
        print("Propriétés :")
        prop_view = props.items()
        print(type(prop_view))
        for item in prop_view:
            print("".rjust(5), item[0], '=', item[1].data)
    print("=====================================================================================================")

    # Changement de la structure d'appel - v0.2
    # Externalisation des propriétés - v0.3
    action = what_action()
    if action != "quit":
        pole = what_pole()
        sprints = what_sprint()
        time = what_time(pole)
        jql = define_jql()
        print(context, "JQL : ", jql)
        match action:
            case "tickets":
                export_issues(pole)
            case "histo":
                export_historique(pole)
