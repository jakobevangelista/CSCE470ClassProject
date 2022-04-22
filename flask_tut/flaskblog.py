from flask import Flask,render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

Bootstrap(app)
class CelebForm(FlaskForm):
    first_name = StringField("First Name: ", validators = [DataRequired()])
    last_name = StringField("Last Name: ", validators = [DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods=('GET', 'POST'))
def index():
    form = CelebForm()
    if form.validate_on_submit():
        name1 = form.first_name.data
        name2 = form.last_name.data
        return redirect(url_for('score', n1 = name1, n2 = name2))
    return render_template("index.html", form=form)

@app.route("/score/<n1>_<n2>")
def score(n1, n2):
    print(n1)
    print(n2)
    return render_template("score.html", first_name = n1, last_name = n2)