import os
import json
from recipe_scrapers import scrape_me
import requests
import urllib
from random import randint

if __name__ == '__main__':
    resp = requests.post('https://d1.supercook.com/dyn/lang_ings',
                         params={'lang': 'pl'})

    # this gives an array of groups that contain a name and a list of ingredients
    ingredient_groups = json.loads(resp.content)

    owned_ingredients = [i for j
                         in ingredient_groups for i in j['ingredients']]  # if randint(0, 20) == 20

    results_req = os.popen(f"curl -s 'https://d1.supercook.com/dyn/results' -X POST -H 'User-Agent: \
        Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0' \
        -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.7,pl;q=0.3' \
        --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: \
        https://www.supercook.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: \
        https://www.supercook.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' \
        -H 'Sec-Fetch-Site: same-site' --data-raw 'needsimage=1&app=1&{urllib.parse.urlencode({'kitchen': ', '.join(owned_ingredients)})}\
        &focus=&kw=&catname=&start=0&fave=false&lang=pl'")

    print(results_req)

    results_req = requests.post('https://d1.supercook.com/dyn/results', headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    }, params={
        'needsimage': 1,
        'app': 1,
        'kitchen': ','.join(owned_ingredients),
        'focus': ' ',
        'kw': ' ',
        'catname': ' ',
        'start': 0,
        'fave': False,
        'lang': 'pl'
    })

    print(results_req.content)

    results = json.loads(results_req.read())['results']

    random_result = results[randint(0, len(results) - 1)]

    details_req = os.popen(f"curl -s 'https://d1.supercook.com/dyn/details' -X POST -H 'User-Agent: \
        Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0' \
        -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.7,pl;q=0.3' \
        --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: \
        https://www.supercook.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H \
        'Referer: https://www.supercook.com/' -H 'Sec-Fetch-Dest: empty' -H \
        'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' --data-raw \
        'rid={random_result['id']}&lang=pl'")

    details = json.loads(details_req.read())
    recipe_hash = details['recipe']['hash']

    scraped = scrape_me(details['recipe']['hash'], wild_mode=True)

    # print()
    # print(details)
    print()
    print(f'{scraped.title()} ({scraped.canonical_url()}):')
    print(scraped.instructions())

    # os.popen('open ' + recipe_hash)
