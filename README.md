# Encyclopedia

## Project description

This script converts `*.md` files into html files and creates static site using Markdown converter + Jinja2 templates.  
[Here](https://yankelevich-dima.github.io/19_site_generator/) you can see generated version of this site.

## How to use

Run `python generate_site.py`.  
With default behavior, script will generate html files from `*.md` files from `/articles/` folder using **config.json**.  
All files will be stored in `./docs/` folder, which is used by GitHub Pages.  

You can change default paths in **config.py**

## Pre-commit hooks

If you need automatical update of your html files after changing `*.md` files, copy `pre-commit` file into `./.git/hooks/` directory.  
It will rebuild all html files, which articles have been changed during commit.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
