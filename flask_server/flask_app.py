import os

from flask import Flask, request, render_template, send_from_directory

from . import page_loader

app = Flask(__name__)


@app.route('/')
def main():
    main_page_content = page_loader.index.load()
    return render_template('main.html', content=main_page_content)


if __name__ == '__main__':
    app.run()
