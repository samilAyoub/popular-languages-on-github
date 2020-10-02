from collections import defaultdict
from datetime import date, timedelta

import requests
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/")
def list_trending_langs():
    """
    Return languages of the 100 trending repos. In which, for each language we
    calculate number of repos using this language and the list of repos using
    the language.
    """

    response = requests.get(
        url="https://api.github.com/search/repositories?q=created:>"
        + str(date.today() - timedelta(days=30))
        + "&sort=stars&order=desc&per_page=100&page=1"
    )
    repos = response.json().get("items")
    d = dict()
    for repo in repos:
        if repo["language"] != None:
            lang = repo["language"]
            repo_name = repo["name"]

            # adding non existing languge
            d[lang] = d.get(lang, {"nbr": 0, "repos": []})

            # updating existing languge
            d[lang].update(
                {"nbr": d[lang]["nbr"] + 1, "repos": d[lang]["repos"] + [repo_name]}
            )
    return make_response(d, 200)


if __name__ == "__main__":
    app.run()
