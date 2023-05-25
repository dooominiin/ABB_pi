import json

with open("OPC/variablen.json", "r", encoding='utf-8') as file:
        variables = json.load(file)
        for var_info in variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = var_info["string"]
            type = var_info["type"]
            print(string)