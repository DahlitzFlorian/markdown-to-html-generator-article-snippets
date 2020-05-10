# main.py

from pathlib import Path

from flask import Flask
from flask import render_template
from flask import send_file

FEEDS_DIR = Path(__file__).parent / "templates" / "feeds"

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/posts/<string:name>")
def blog_post(name: str):
    return render_template(f"posts/{name}.html")


@app.route("/feeds/blog")
def blog_feed():
    return send_file(FEEDS_DIR / "rss.xml")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
