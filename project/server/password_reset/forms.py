from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo
)


class RequestResetForm(FlaskForm):
    email = StringField("Email Address", [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField('Reset Password')
