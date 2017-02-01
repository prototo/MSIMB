from msimb.models import User
from msimb import db


admin = User.query.filter_by(username='admin').first()
if not admin:
    print("admin user not found")
    admin = User('admin', 'admin')
    db.session.add(admin)
    db.session.commit()
    print("admin user created")
