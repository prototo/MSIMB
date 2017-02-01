from msimb import db
from msimb.models.Note import Note
from msimb.models.User import User


__all__ = ['Note', 'User']

db.create_all()
