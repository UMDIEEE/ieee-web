from flask_wtf import Form
from wtforms import BooleanField, TextField, SubmitField, validators

class TestbankSettingsForm(Form):
    gdrive_folder = TextField('Google Drive Folder:', [validators.Length(min=1)])
    confirm_change = BooleanField('Confirm Change', [validators.Required()])
    submit = SubmitField("Save")
