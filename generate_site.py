import os
import argparse

import markdown
from jinja2 import Environment, FileSystemLoader

from config import ARTICLES, ARTICLES_PATH, TEMPLATE_PATH, TOPICS_MAP, HTML_PATH


def markdown_to_html(path):
    with open(path, 'r') as md_file:
        md_data = md_file.read()
    return markdown.markdown(md_data, extensions=['markdown.extensions.codehilite'])


def render_html_from_template(template, data={}):
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template(template)
    return template.render(**data)


def save_html(html_data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as htmlfile:
        htmlfile.write(html_data)


def generate_article_page(article):
    article_content = markdown_to_html(os.path.join(ARTICLES_PATH, article['source']))
    article_html = render_html_from_template('article.html', {
        'content': article_content,
        'title': article['title'],
        'topic': TOPICS_MAP[article['topic']]
    })
    path = os.path.join(HTML_PATH, article['source'].replace('.md', '.html'))
    save_html(article_html, path)


def update_article_page(article_source):
    try:
        article = [element for element in ARTICLES if element['source'] == article_source][0]
        generate_article_page(article)
    except IndexError:
        raise OSError('No such file {}'.format(article_source))


def generate_index_page():
    topics = {element: [] for element in TOPICS_MAP.values()}
    for article in ARTICLES:
        article['path'] = article['source'].replace('.md', '.html')
        topics[TOPICS_MAP[article['topic']]].append(article)
    index_html = render_html_from_template('index.html', {
        'topics': topics
    })
    path = os.path.join(HTML_PATH, 'index.html')
    save_html(index_html, path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--update', type=str, help='Input article to update')

    args = parser.parse_args()

    if args.update:
        update_article_page(args.update)

    else:
        generate_index_page()
        for element in ARTICLES:
            generate_article_page(element)
