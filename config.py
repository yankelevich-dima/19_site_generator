import json

with open('config.json', 'r') as jsonfile:
    data = json.load(jsonfile)

TOPICS_MAP = {element['slug']: element['title'] for element in data['topics']}
ARTICLES = data['articles']

ARTICLES_PATH = './articles/'
TEMPLATE_PATH = './templates/'

HTML_PATH = './docs/'
