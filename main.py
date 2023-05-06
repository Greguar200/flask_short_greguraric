from flask import Flask, render_template
import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
import string

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)

class URLmodel (db.Model):

    id = db.Column(db. Integer, primary_key=True)
    original_url = db.Column (db.String(255), unique=True)

    short = db.Column(db.String(6), unique=True)
    visits = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    return render_template('urls.html')


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    url = URLmodel.query.filter(URLmodel.short == short).first()
    if url:
        url.visits += 1
        db.session.add(url)
        db.session.commit()
        return redirect(url.original_url)


@app.route('/urls', methods=['GET'])
def urls():
    urls = URLmodel.query.all()
    return render_template('urls.html', urls=urls)

class URLForm(FlaskForm):

    original_url = StringField('Bстовьте ссылkу',
                                        validators=[DataRequired(message='Cсonka He MoжеT бuть пустOй'),
                                        URL (message='Невернaя ссunka')])
    submit = SubmitField('Получить короткую ссылку')

def get_short():
    while True:
        short = ''.join(random.choices(string.ascii_letters + string.ascii_letters, k=6))
        if URLmodel.query.filter(URLmodel.short == short).first():
            continue
        return short



if __name__ == '__main__':
    app.run()
