from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class ImageUploadForm(FlaskForm):
    image_file = FileField(label="上傳圖片：", validators=[FileRequired()])
    submit = SubmitField(label="上傳")
