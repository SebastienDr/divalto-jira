from jiraone import LOGIN, PROJECT
import csv

user = "sdrouard.ext"
password = "SOP1_Avecesar1"
link = "https://jira.soprema.ca"
LOGIN.api = False  # comment out line, if you want to extract history from a cloud instance
LOGIN(user=user, password=password, url=link)

if __name__ == '__main__':
      projectDivalto = "project = DIVALTO AND"
      # the output of the file would be absolute to the directory where this python file is being executed from
      #jql = projectDivalto + " Sprint in (255, 257, 258, 265, 267, 272, 273, 282, 290, 292, 295, 296, 297, 305, 319)" # Sprints 2 à 16 - SOE
      #jql = projectDivalto + " Sprint in (275, 277, 283, 298, 304, 320, 325)" # Sprints 1 à 7 - Finance
      #jql = projectDivalto + " Sprint in (262, 263, 266, 271, 274, 281, 289, 291, 299, 306, 307, 317, 321, 324)" # Sprint SOI-Eu
      jql = projectDivalto + " Sprint in (293, 300, 308, 310, 318, 322, 330)" # Sprints SopCa
      PROJECT.change_log(jql=jql)

