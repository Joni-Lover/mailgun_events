#!/usr/bin/env python3
import os
import sys
import requests
import json

if len(sys.argv) != 1:
    print("Usage: mailgun_events.py 'api-key' 'example.com'")
    sys.exit(1)

filename = "result.json"

api_key = sys.argv[1]
domain = sys.argv[2]
filters = sys.argv[3]

url = "https://api.mailgun.net/v3/%s/events"
url = url % domain
params = {"event": filters, "limit": 300}

items = []
last_next_url = None
count = 0
while url is not last_next_url:
    r = requests.get(
        url,
        auth=("api", api_key),
        params=params
    )

    items += r.json()["items"]
    print(count)

    if 200 == r.status_code and not len(r.json()["items"]) == 0:
        url = r.json()["paging"]['next']
    count += count + 1

if items != 0:
    with open(filename, "w") as outfile:
        json.dump(items, outfile)
