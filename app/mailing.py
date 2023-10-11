from app import mail
from flask_mail import Message
import flask



def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    send_email('Password reset',
               sender="mymail@gmail.com",
               recipients=[user.email],
               text_body=flask.render_template('email/reset_password.txt', user=user),
               html_body=flask.render_template('email/reset_password.html', user=user))