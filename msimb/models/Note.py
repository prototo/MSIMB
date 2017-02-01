from msimb import db
import datetime


SPAM_TIMEDELTA = datetime.timedelta(minutes=5)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=True)
    approved = db.Column(db.Boolean(), default=False, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.datetime.utcnow, nullable=False)
    approved_date = db.Column(db.Date(), nullable=True)
    from_ip = db.Column(db.Text)

    def __init__(self, text, image=None, from_ip=None):
        self.text = text
        self.image = image
        self.from_ip = from_ip

    def __repr__(self):
        return self.text

    @classmethod
    def is_spam(self, from_ip):
        try:
            last_note = self.query.filter(
                Note.from_ip == from_ip
            )[-1]
        except:
            return False
        delta = datetime.datetime.utcnow() - last_note.created
        if delta < SPAM_TIMEDELTA:
            return 'Sorry, you can\'t post more than once every 5 minutes'
        return False
