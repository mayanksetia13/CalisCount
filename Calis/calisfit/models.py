from calisfit import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    mybody = db.relationship('Cred', backref='user', lazy=True)

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


class Cred(db.Model):
    cred_id = db.Column(db.Integer,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False,
                     server_default=db.func.now())
    activity = db.Column(db.String(20), nullable=False)
    bmr = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)

    def cal(self, gender):
        self.cal_bmr(gender)
        self.cal_cal()

    def cal_cal(self):
        self.calories = self.bmr * {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "super": 1.9
        }.get(self.activity)
        self.calories = round(self.calories, 2)

    def cal_bmr(self, gender):
        if gender == 'M':
            self.bmr = (10 * self.weight) + \
                (6.25 * self.height) - (5 * self.age) + 5
            self.bmr = round(self.bmr, 2)
            return None

        self.bmr = (10 * self.weight) + \
            (6.25 * self.height) - (5 * self.age) - 161
        self.bmr = round(self.bmr, 2)

    def __repr__(self):
        return f"{self.cred_id}, {self.user_id}, {self.height}, {self.weight}, {self.age}, {self.time}, {self.bmr}, {self.calories}"
