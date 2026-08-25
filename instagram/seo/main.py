#!/usr/bin/env python3

import json
import random
from rich import print

data_json = "data.json"

min_ht = 13
max_ht = 19

min_kw = 11
max_kw = 17

anchor_ht = ["#irklost", "#irklostNYC", "#irklostArtist", "#nemoAKAirklost"]
anchor_kw = ["irklost", "nemo aka irklost", "nemo the artist"]

def main():
    with open(data_json, "r") as file:
        data = json.load(file)
    cats = list(data.keys())
    for idx,cat in enumerate(cats):
        print(idx, cat)
    cat_choice = int(input())
    if cat_choice < 0 or cat_choice >= len(cats):
        cat_choice = 0
    ht = list(data[cats[cat_choice]].keys())[0]
    kw = list(data[cats[cat_choice]].keys())[1]
    ht_all = list(data[cats[cat_choice]][ht])
    kw_all = list(data[cats[cat_choice]][kw])
    ht_num = random.randint(min_ht,max_ht)
    kw_num = random.randint(min_kw,max_kw)
    ht_list = random.choices(ht_all,k=ht_num)
    kw_list = random.choices(kw_all,k=kw_num)
    ht_list += anchor_ht
    kw_list += anchor_kw
    print(f"\n\n---COPY AND PASTE THE BELOW LINES FOR A <<< {cats[cat_choice]} >>> POST. CAPTION FOR POST, COMMENTS FOR STORIES AND REELS---\n\n")
    print(" ".join(ht_list))
    print(", ".join(kw_list))


if __name__ == "__main__":
    main()
