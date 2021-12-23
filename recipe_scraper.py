import json
from recipe_scrapers import scrape_me
import requests
from random import randint

if __name__ == '__main__':
    resp = requests.post(
        'https://d1.supercook.com/dyn/lang_ings', data={'lang': 'pl'})

    # this gives an array of groups that contain a name and a list of ingredients
    ingredient_groups = json.loads(resp.content)

    owned_ingredients = [i for j
                         in ingredient_groups for i in j['ingredients'] if randint(0, 9) <= 2]  # if randint(0, 20) == 20

    results_req = requests.post('https://d1.supercook.com/dyn/results', headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    }, data={
        'needsimage': 1,
        'app': 1,
        'kitchen': ','.join(owned_ingredients),
        'focus': '',
        'kw': '',
        'catname': '',
        'start': 0,
        'fave': False,
        'lang': 'pl'
    })

    results = json.loads(results_req.content)['results']
    random_result = results[randint(0, len(results) - 1)]

    details_req = requests.post('https://d1.supercook.com/dyn/details', headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    }, data={
        'rid': random_result['id'],
        'lang': 'pl'
    })

    details = json.loads(details_req.content)
    recipe_hash = details['recipe']['hash']

    scraped = scrape_me(details['recipe']['hash'], wild_mode=True)

    print()
    print(f'{scraped.title()} ({scraped.canonical_url()}):')
    print(scraped.instructions())
