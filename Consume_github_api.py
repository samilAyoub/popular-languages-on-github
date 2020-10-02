from datetime import date, timedelta
from collections import defaultdict
import requests
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route("/")
def list_trending_lang():
    response = requests.get(
        url="https://api.github.com/search/repositories?q=created:>"
        + str(date.today() - timedelta(days=30))
        + "&sort=stars&order=desc&per_page=100&page=1"
    )

    repos = response.json().get('items')
    d = {}
    for repo in repos:
        if repo['language'] != None:
            lang = repo['language']
            repo_name = repo['name']
            d[lang] = d.get(lang, {'nbr': 0,
                                   'repos': []})
            d[lang].update({'nbr': d[lang]['nbr'] + 1,
                            'repos': d[lang]['repos'] + [repo_name]})

    return make_response(d, 200)


if __name__ == "__main__":
    app.run()
