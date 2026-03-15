from flask import Flask, render_template, send_file
from datetime import datetime
import os

app = Flask(__name__)

SUMMARY_FILE = "../out2.txt"


def generate_summary():

    with open(SUMMARY_FILE, "w") as f:
        # f.write(text)
        f.write(f"Summary generated at {datetime.now().isoformat()}\n\n")

    # return text


@app.route("/")
def home():
    if not os.path.exists(SUMMARY_FILE):
        content = generate_summary()
    else:
        with open(SUMMARY_FILE) as f:
            content = f.read()

    return render_template("index.html", content=content)


@app.route("/download")
def download():
    return send_file(SUMMARY_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
