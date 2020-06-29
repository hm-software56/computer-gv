from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class Upload(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['mp4', 'avi', 'mkv'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    photo = FileField('', validators=validators)
