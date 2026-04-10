from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

import os
import smtplib
from email.message import EmailMessage





app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


class ContactForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired()])
    message = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Send Message')

@app.route('/', methods=['GET','POST'])
def index():
    form = ContactForm()
    lines = range(0,56)

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = f'Message from {name} - {email}'
        msg['From'] = "automation.practice.bot@gmail.com"
        msg['To'] = "paritoshpalai07@gmail.com"

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Secure the connection
                server.login("automation.practice.bot@gmail.com", os.getenv('GMAIL_APP_PASSWORD'))
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")

        return redirect(url_for('index'))

    return render_template('index.html', lines=lines, form=form)
