from flask import Flask , render_template , url_for 
from forms import RegistrationForm , LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']='5462e873044b87176bfddd4951719708'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	form = RegistrationForm()
	return render_template('register.html',title='Register',form=form)

@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html',title='Login',form=form)	

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/body')
def body():
	return render_template('body.html')

@app.route('/learn')
def learn():
	return render_template('learn.html')		

if __name__ == "__main__":
	app.run(debug=True)