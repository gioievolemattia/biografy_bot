from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Feedback(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    feedback = Feedback(name=name, email=email, message=message)
    db.session.add(feedback)
    db.session.commit()

    return redirect(url_for('feedback_success'))
@app.route('/feedback_success')
def feedback_success():
    return render_template('feedback_success.html')

with app.app_context():
    db.create_all()

import os

if __name__ == "__main__":
    # Railway assegna una porta variabile, questo codice la intercetta
    port = int(os.environ.get("PORT", 5000))
    # '0.0.0.0' serve per rendere il sito visibile all'esterno
    app.run(host='0.0.0.0', port=port)