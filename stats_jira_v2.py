from jiraone import LOGIN, PROJECT
import csv

def whatPole() -> str:

    print("Pour quel pôle veux-tu extraire les données ? ALL ou", list(poles.keys()))
    pole = input('Pôle : ')

    # On vérifie que l'user ne tape pas de la me*de
    while (pole != "ALL" and pole not in poles.keys()):
         print ("Pôle inconnu, veuillez entrer une des clés : ALL ou",list(poles.keys()))
         pole = input('Pôle : ')
         
    return pole

def showPole(pole):
  print("")
  print("====================================",poles.get(pole),"====================================")
  # Extraction du projet
  print("==> Extraction du projet",poles.get(pole),"...")
 
def defineJql(pole) -> str:
  projectDivalto = "project = DIVALTO AND "
  if (pole == 'SOE'):
       sprints = "Sprint in (255, 257, 258, 265, 267, 272, 273, 282, 290, 292, 295, 296, 297, 305, 319)" # Sprints 2 à 16 - SOE
  elif (pole == 'FIN'):
       sprints = "Sprint in (275, 277, 283, 298, 304, 320, 325)" # Sprints 1 à 7 - Finance
  elif (pole == 'SOI'):
       sprints = "Sprint in (262, 263, 266, 271, 274, 281, 289, 291, 299, 306, 307, 317, 321, 324)" # Sprints SOI-Eu
  elif (pole == 'SOPCA'):
       sprints = "Sprint in (293, 300, 308, 310, 318, 322, 330)" # Sprints SopCa
  elif (pole == 'INFRA'):
       sprints = "labels = DIVALTO_INFRA AND statusCategory not in (Done)"
  else:
      print("Pas de pôle reconnu...!")

  jql = projectDivalto + sprints
  return jql

def exportIssues(pole):
  showPole(pole)
  
  fileName = str(poles.get(pole)) +"_Tickets" # Fichier de sortie des données des tickets
  
  # Tickets
  PROJECT.export_issues(jql=jql, folder=destinationFolder, final_file=fileName+extension)
  
def exportHistorique(pole):
  fileNameHisto = str(pole) +"_Historique" # Fichier de sortie des données de l'historique des tickets
  # Historique des tickets
  PROJECT.change_log(folder=destinationFolder, file=fileNameHisto+extension, jql=jql)

# JIRA : URL et login
user = "sdrouard.ext"
password = "SOP1_Avecesar1"
link = "https://jira.soprema.ca"
LOGIN.api = False  # comment out line, if you want to extract history from a cloud instance
LOGIN(user=user, password=password, url=link)

# Gestion des fichiers
destinationFolder="Divalto"
extension = ".txt" # Pour le moment : pour éviter les problèmes d'encoding

# Liste des pôles
poles = {}
poles['SOI'] = 'SOI'
poles['SOE'] = 'SOE'
poles['FIN'] = 'Finance'
poles['SOPCA'] = 'SopCa'
poles['INFRA'] = 'Infra'

# Pôle sur lequel sortir les données
pole = whatPole()

# Programme principal
if __name__ == '__main__':

  # Requete JQL
  jql = defineJql(pole)
  if (pole != "ALL"):
    exportIssues(pole)
    exportHistorique(pole)
  else:
    for p in list(poles.keys()):
       exportIssues(p)
       exportHistorique(p)