from calisfit import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    #mybody = db.relationship('Cred',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def create_db(debug=False):
        try:
            number_of_users = len(User.query.all())
            if number_of_users >= 0:
                if debug:
                    print(f"User Table Exists with {number_of_users} Users!")
            return True
        except:
            db.create_all()
            return False
            
"""class Cred(db.Model):
	height = db.Column(db.Integer,nullable=False)
	weight = db.Column(db.Integer,nullable=False)
	#user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f"Cred('{self.height}','{self.weight}')"
"""
