#codeng:utf-8

from wtforms import Form, TextField, TextAreaField
from wtforms.validators import Required, Length

class EditForm(Form):
	title = TextField(u"title", validators=[
            Required(u"input title"),
            Length(min=1, max=100, message=u"under 100")
        ])
	member = TextField(u"member", validators=[
            Required(u"input member")
        ])

