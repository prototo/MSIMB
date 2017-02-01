export FLASK_APP=msimb/app.py
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db'
flask run --host=0.0.0.0
