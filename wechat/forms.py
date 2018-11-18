from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class sendForm(FlaskForm):
    name = StringField('收信者姓名', validators=[DataRequired(), Length(1, 20)])
    message = TextAreaField('请输入发送的信息', validators=[DataRequired(), Length(1,1000)])
    submit = SubmitField('发送 Send')
