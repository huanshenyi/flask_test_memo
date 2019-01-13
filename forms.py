#!/usr/bin/python
#coding=utf-8



from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    """ 内容フォーム """
    title = StringField(label='タイトル', validators=[DataRequired("タイトルを入力してください")],
        description="タイトルを入力してください",
        render_kw={"required": "required", "class": "form-control"})
    content = TextAreaField(label='内容', validators=[DataRequired("内容を入力してください")],
        description="内容を入力してください",
        render_kw={"required": "required", "class": "form-control"})
    type = SelectField('カテゴリー',
        choices=[('オススメ', 'オススメ'), ('python', 'python'), ('php', 'php'), ('Go', 'Go')],
        render_kw={'class': 'form-control'})
    image= StringField(label='画像',
        description='画像urlを入力してください',
        render_kw={'required': 'required', 'class': 'form-control'})
    """表示するかどうかのオプション"""
    is_valid = SelectField('表示するか',
        choices=[('1', '表示する'), ('0', '表示しない')],
        render_kw={'class': 'form-control'})
    submit = SubmitField('提出')

