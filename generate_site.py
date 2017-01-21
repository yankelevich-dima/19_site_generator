import os
import json
import argparse

import markdown
from jinja2 import Environment, FileSystemLoader

ARTICLES_PATH = './articles/'
TEMPLATE_PATH = './templates/'

HTML_PATH = './docs/'
JSON_PATH = 'config.json'


def get_json_config(path):
    with open(path, 'r') as jsonfile:
        return json.load(jsonfile)


def parse_json_config(json_config):
    topics_map = {element['slug']: element['title'] for element in json_config['topics']}
    articles = json_config['articles']
    return articles, topics_map


def rename_extension(path, new_extension):
    """
    rename_extension('path/to/file.ext', '.new') -> 'path/to/file.new'
    """
    root, ext = os.path.splitext(path)
    return root + new_extension


def get_markdown_content(path):
    with open(path, 'r') as md_file:
        return md_file.read()


def markdown_to_html(path):
    md_data = get_markdown_content(path)
    return markdown.markdown(md_data, safe_mode='escape', extensions=['markdown.extensions.codehilite'])


def render_html_from_template(template, data={}):
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(template)
    return template.render(**data)


def save_html(html_data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as htmlfile:
        htmlfile.write(html_data)


def generate_article_page(article, topics_map):
    article_content = markdown_to_html(os.path.join(ARTICLES_PATH, article['source']))
    article_html = render_html_from_template('article.html', {
        'content': article_content,
        'title': article['title'],
        'topic': topics_map[article['topic']]
    })
    path = os.path.join(HTML_PATH, rename_extension(article['source'], '.html'))
    save_html(article_html, path)


def update_article_page(article_source, articles, topics_map):
    try:
        article = [element for element in articles if element['source'] == article_source][0]
        generate_article_page(article, topics_map)
    except IndexError:
        raise OSError('No such file {}'.format(article_source))


def generate_index_page(articles, topics_map):
    topics = {element: [] for element in topics_map.values()}
    for article in articles:
        article_data = {}
        article_data['path'] = rename_extension(article['source'], '.html')
        article_data['title'] = article['title']
        topics[topics_map[article['topic']]].append(article_data)
    index_html = render_html_from_template('index.html', {
        'topics': topics
    })
    path = os.path.join(HTML_PATH, 'index.html')
    save_html(index_html, path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--update-articles', dest='article_list', type=str, nargs='*', help='Input articles to update')

    args = parser.parse_args()

    config = get_json_config(JSON_PATH)
    articles, topics_map = parse_json_config(config)

    if args.article_list:
        for article in args.article_list:
            update_article_page(article, articles, topics_map)

    else:
        generate_index_page(articles, topics_map)
        for element in articles:
            generate_article_page(element, topics_map)
