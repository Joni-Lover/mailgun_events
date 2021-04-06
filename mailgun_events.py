#!/usr/bin/env python3

import json
import requests
import sys
from os import path

if len(sys.argv) != 4:
    print("Usage: mailgun_events.py 'api-key' 'example.com' 'rejected OR failed'")
    sys.exit(1)

filename = "result.json"
page_url = 'page_url.txt'

api_key = sys.argv[1]
domain = sys.argv[2]
filters = sys.argv[3]

url = "https://api.mailgun.net/v3/%s/events"
url = url % domain
params = {"event": filters}

item = []
last_next_url = None
count = 0

if path.exists(page_url) and path.getsize(page_url) > 0:
    f = open(page_url, "r")
    url = f.readline()
    print(url)

while url is not last_next_url:
    r = requests.get(
        url,
        auth=("api", api_key),
        params=params
    )

    item += r.json()["items"]
    print(count)
    print(url)

    if item != 0:
        if path.exists(filename) and path.getsize(filename) > 0:
            with open(filename, "r+") as outfile:
                    data = json.load(outfile)
                    data.append(item)
                    outfile.seek(0)
                    json.dump(data, outfile)
                    print('Update results')
        else:
            with open(filename, "w") as outfile:
                json.dump(item, outfile)
                print('Init results')


    if 200 == r.status_code and not len(r.json()["items"]) == 0:
        url = r.json()["paging"]['next']
        f = open(page_url, "w")
        f.write(url)
        f.close()
    count += count + 1

