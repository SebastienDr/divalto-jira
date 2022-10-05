import yaml

with open(r'./properties/test.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    testlist = yaml.load(file, Loader=yaml.FullLoader)

    print(testlist.get('jira.user'))
