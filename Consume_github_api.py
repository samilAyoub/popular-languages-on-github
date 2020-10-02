
from flask import Flask, request
from datetime import date, timedelta

import requests

app = Flask(__name__)


@app.route("/")
def list_trending_repos():
    response = requests.get(
        url="https://api.github.com/search/repositories?q=created:>"
        + str(date.today() - timedelta(days=30))
        + "&sort=stars&order=desc"
    )
    return response.json()


if __name__ == "__main__":
    app.run()
