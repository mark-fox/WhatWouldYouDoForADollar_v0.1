from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import dbcode



# Run database creation method at startup.
dbcode.create_table()

app = Flask(__name__, '/static', static_folder='static', template_folder='templates')
# Secret key used for wtforms' login.
app.config['SECRET_KEY'] = 'ImNotGivingASecretToAMachine!'
# Establishes database location.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.sqlite'
Bootstrap(app)
# Not used at this time.
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flag variable to determine what to display based on login credentials.
# To be implemented later.
loggedIn = False



# Classes to create wtforms with validations.
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=15)])
    # TODO increase password min once done testing/developing
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=80)])

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=15)])
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=2, max=15)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=2, max=15)])
    # TODO increase password min once done testing/developing
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=80)])




# Home page route.
@app.route('/')
def home():
    return render_template('homebase.html', loggedIn=loggedIn)



# Route for pressing New Task button.
@app.route('/newtask', methods=['POST'])
def new_task():
    return render_template('newtask.html')



# Route for pressing View Tasks button.
@app.route('/viewtasks', methods=['POST'])
def view_tasks():
    # Runs query on database and passes results to page.
    data = dbcode.select_all_db()
    return render_template('viewtasks.html', tasks=data)



# Individual task page.
@app.route('/task/<string:id>/')
def showTasks(id):
    # Runs query on database for the matching data.
    data = dbcode.select_id_db(id)
    return render_template('task.html', id=id, task=data)




# Route for displaying confirmation after making new task.
@app.route('/madeit', methods=['POST'])
def madeTask():
# TODO move time and other stuff out of methods and add here
    # Retrieves user inputs.
    taskname = request.form['tasknameInput']
    descript = request.form['descriptInput']

# TODO switch out with username eventually
    seller = 'Guest'

    fare = request.form['fareInput']
    duration = request.form['durationInput']

    if taskname == "" or descript == "" or fare == "" or duration == "":
        return render_template('newtask.html', error="Please fill in all fields.")

    # Runs query to add values to database.
    dbcode.add_task_db(taskname, descript, seller, fare, duration)
    # Retrieves the database entry that was just added.
    madeatask = dbcode.select_taskname_db(taskname)
    return render_template('madenewtask.html', task=madeatask)




# Route for confirmation page after committing to tasks.
@app.route('/soulsold', methods=['GET', 'POST'])
def sellSoul():
    # Retrieves checkbox values that are checked.
    # Each checkbox's value is the id number for that row's data.
    data = request.form.getlist("cbox")

# TODO figure out easier way:
    # Loops through results and runs separate query to update field.
    for i in data:
        dbcode.close_task_db(i)
    return render_template('receipt.html')




# Route for about page that is in the works.
@app.route('/about')
def about():
    return render_template('about.html')


# Route for contact page that is in the works.
@app.route('/contact')
def contact():
    return render_template('contact.html')




# Route for login page that uses validation.
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        print('login validate passed')
        # TODO implement login validation.

    return render_template('login.html', form=loginform)



# Route for signup page that uses validation.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignupForm()
    if signupform.validate_on_submit():
        print('signup validate success')
        # TODO implement signup validation.

    return render_template('signup.html', form=signupform)


# Route for logging out.
@app.route('/logout')
def logout():
    logout_user()
    return render_template('homebase.html', loggedIn=loggedIn, name='Guest')



# Runs app.
if __name__ == '__main__':
    app.run(debug=True)




# references:
    # button redirects - https://stackoverflow.com/questions/19794695/flask-python-buttons
    # tasks table outline - https://datatables.net/examples/basic_init/scroll_y.html
    # some SQLAlchemy setup - https://www.youtube.com/watch?v=PJK950Gp780
    # unix time - http://avilpage.com/2014/11/python-unix-timestamp-utc-and-their.html
    # database setup - https://www.youtube.com/watch?v=xTumGVC90_0
    # database setup - https://www.youtube.com/watch?v=qfGu0fBfNBs
    # amazing login and database setup - https://www.youtube.com/watch?v=8aTnmsDMldY
    # row_factory - https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
    # request.form.getlist - https://stackoverflow.com/questions/7996075/iterate-through-checkboxes-in-flask
    # css for table - http://johnsardine.com/freebies/dl-html-css/simple-little-tab/
    #