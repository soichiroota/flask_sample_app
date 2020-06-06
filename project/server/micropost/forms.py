from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField
from wtforms.validators import Length
from flask_uploads import UploadSet, IMAGES


images = UploadSet('images', IMAGES)


class CreateMicropostForm(FlaskForm):
    content = TextAreaField("", [
        Length(max=140)
    ])
    picture = FileField('', validators=[
        FileAllowed(images, 'Images only!')
    ])
