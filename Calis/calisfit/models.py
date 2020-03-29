import secrets
import os
import os.path
from PIL import Image
from calisfit import db, login_manager
from flask_login import UserMixin
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default='default.png')
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

    @staticmethod
    def save_picture(app, form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(
            app.root_path, 'static/profile_pics', picture_fn)
        dir_path = os.path.join(app.root_path, 'static/profile_pics')

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)

        i.save(picture_path)

        return picture_fn


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

    def display_histogram(self, id, tracks, app):

        # get all records from db
        tracks = tracks.all()

        dir_path = os.path.join(app.root_path, 'static/graphs')
        plt.style.use('seaborn-deep')

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        graph_name = f"{self.cred_id}-{self.user_id}-{self.time.isoformat()}.png"
        graph_path = os.path.join(dir_path, graph_name)

        # if os.path.exists(graph_path):
        #     return graph_name

        bins = 20

        x = [i.bmr for i in tracks]
        y = [i.calories for i in tracks]

        plt.hist([x, y], bins, label=['BMR', 'Calories'], )

        plt.legend(loc='upper right')

        plt.savefig(graph_path)

        plt.close()

        return graph_name

    def __repr__(self):
        return f"{self.cred_id}, {self.user_id}, {self.height}, {self.weight}, {self.age}, {self.time}, {self.bmr}, {self.calories}"
