from agenda import app
from flask import url_for, render_template

@app.route("/")
def home():
    return render_template('base.html')

