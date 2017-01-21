import json

with open('config.json', 'r') as jsonfile:
    config_data = json.load(jsonfile)

TOPICS_MAP = {element['slug']: element['title'] for element in config_data['topics']}
ARTICLES = config_data['articles']

ARTICLES_PATH = './articles/'
TEMPLATE_PATH = './templates/'

HTML_PATH = './docs/'
