from flask import Flask
from flask_sqlalchemy import SQLAlchemy


__all__ = ['db', 'app']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = 'qweasd123456'
db = SQLAlchemy(app)

