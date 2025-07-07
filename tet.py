
import json 

with open("boats/test/test.json", "r") as f:
    test = json.load(f)
print(test[0])