# main.py

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/posts/<string:name>")
def blog_post(name: str):
    return render_template(f"posts/{name}.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
