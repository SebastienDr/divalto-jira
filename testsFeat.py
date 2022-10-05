import yaml
from jproperties import Properties

configs = Properties()

with open(r'properties/stats_jira.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    testlist = yaml.load(file, Loader=yaml.FullLoader)

    print("- open with pyyaml :", testlist.get('jira.user'))

with open('properties/stats_jira.properties', 'rb') as config_file:
    configs.load(config_file)

    print("- open with jproperties :", configs.get('showProperties').data)

