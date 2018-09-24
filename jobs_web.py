#!/usr/bin/env python3
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def show_jobs():
    jobs = sqlite3.connect('jobs.db').cursor().execute('SELECT * FROM jobs')
    return render_template('index.html', jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
