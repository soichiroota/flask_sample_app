from flask_mail import Message
from flask import url_for, current_app

from project.server import mail


class UserMailer:
    @classmethod
    def account_activation(cls, user):
        token = user.get_token(expires_sec=7200)
        msg = Message(
            'Account activation',
            sender=current_app.config.get('MAIL_USERNAME'),
            recipients=[user.email]
        )
        msg.body = '''Hi {user_name}, Welcome to the Sample App!
Click on the link below to activate your account:
{url}'''.format(
            user_name=user.name,
            url=url_for(
                'account_activation.edit',
                token=token,
                _external=True
            )
        )
        mail.send(msg)

    @classmethod
    def password_reset(cls, user):
        token = user.get_token(expires_sec=7200)
        msg = Message(
            'Password Reset',
            sender=current_app.config.get('MAIL_USERNAME'),
            recipients=[user.email]
        )
        msg.body = '''To reset your password, visit the following link: {url}
If you did not make this request,
then simply ignore this email and no change will be made.
'''.format(
            url=url_for(
                'password_reset.edit',
                token=token,
                _external=True
            )
        )
        mail.send(msg)
