import json

with open('fehler.json', 'r') as c:
    obj = json.load(c)
    print("fehler.json :::::::::")
    for content in obj["content"]:
        if "manufacturerModelId" in content == True:
            print("JA")
        else:
            print("NEIN")
        print(content["manufacturerModelId"]["name"])
