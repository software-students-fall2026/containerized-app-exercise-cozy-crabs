"""Stub Flask app for the subsystem"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Return a Hello World message"""
    return render_template("index.html")


@app.route("/record")
def record():
    """Show the microphone recorder."""
    return render_template("record.html")


if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000)
