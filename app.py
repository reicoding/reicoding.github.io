from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates')
# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_partner_finder.db'
db = SQLAlchemy(app)

# Define a model for your tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)

# Make sure to create the database file and tables

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get task description from the form
        task_description = request.form['task']
        # Create a new task instance
        new_task = Task(description=task_description)
        # Add it to the database
        db.session.add(new_task)
        db.session.commit()
        # Redirect to home to display the task list
        return redirect(url_for('home'))
    else:
        # Get all tasks from the database
        tasks = Task.query.all()
        # Render the home page template with the tasks
        return render_template('home.html', tasks=tasks)

@app.route('/test', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return 'Ini adalah POST request!'
    else : 
        return 'Hello, World! Ini adalah GET request.'

#####
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Relationship with other tables
    tasks = db.relationship('Task', backref='author', lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

###
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
###
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

