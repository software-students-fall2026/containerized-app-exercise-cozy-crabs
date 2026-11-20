"""Stub Flask app for the subsystem"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Return a Hello World message"""
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
