#!/usr/bin/env python3

import json
from rich import print

data_json = "data.json"

def main():
    with open(data_json, "r") as file:
        data = json.load(file)
    #print(json.dumps(data,indent=4))
    print(len(data))
    print(data.keys())


if __name__ == "__main__":
    main()
