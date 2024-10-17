from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


@app.route("/")  # defines the route of the page that runs de function below.
def home():
    return render_template("index.html")


@app.route('/bye')
def bye_world():
    return 'Bye, world.'


if __name__ == "__main__":
    app.run(debug=True)

