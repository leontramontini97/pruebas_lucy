from flask import Flask, render_template, redirect, url_for, request, session
from models import Conversation, db  # Import db from models.py
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import timedelta
import os

# Initialize app
app = Flask(__name__)

# Set up secret key and database configuration
app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admindialogik:Citasautomaticas.1@mensajes-chatbots.cxs28aauwxi4.us-east-2.rds.amazonaws.com:5432/lucy_abdala')

# Initialize the db with the Flask app
db.init_app(app)

# Create tables with Flask-SQLAlchemy in an app context
with app.app_context():
    db.create_all()

# Logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SESSION_COOKIE_SECURE'] = False


# Session timeout
app.permanent_session_lifetime = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "dialogik" and password == "123":
            session['logged_in'] = True
            return redirect('/flask/dashboard')

        else:
            return "Invalid credentials"
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        page = request.args.get('page', 1, type=int)  # Get the current page number
        conversations = Conversation.query.paginate(page=page, per_page=10)  # Paginate results
    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        return render_template('error.html', error="Error fetching data from the database")

    return render_template('dashboard.html', conversations=conversations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
