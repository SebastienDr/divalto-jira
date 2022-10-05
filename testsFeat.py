import yaml

with open(r'properties/stats_jira.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    testlist = yaml.load(file, Loader=yaml.FullLoader)

    print("- open with pyyaml :", testlist.get('jira.user'))
