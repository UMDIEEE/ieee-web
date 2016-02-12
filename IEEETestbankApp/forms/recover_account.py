from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email, Length, NumberRange

class RecoverAccountForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    dirid = TextField('UMD Directory ID', validators=[Required(), Regexp(r'[0-9A-Za-z]+')])
    uid = TextField('UID', validators=[Required(), Length(min=9, max=9), NumberRange(min=0, max=999999999)])
