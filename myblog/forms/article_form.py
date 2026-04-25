from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField(label="標題：", validators=[DataRequired()])
    content = TextAreaField(label="內容：", validators=[DataRequired()])
    submit = SubmitField(label="發佈")
