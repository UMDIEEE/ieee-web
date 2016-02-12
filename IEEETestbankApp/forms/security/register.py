from wtforms import StringField, SelectField, IntegerField
from flask_security.forms import Form, RegisterFormMixin, ConfirmRegisterForm, Required

major_choices = [ ("elecengr", "Electrical Engineering"),
                  ("compengr", "Computer Engineering"),
                  ("compsci",  "Computer Science"),
                  ("other",    "Other")
                ]

grad_semester_choices = [ ("fall", "Fall"), ("spring", "Spring") ]

class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])

class UMDConfirmRegisterForm(Form, RegisterFormMixin):
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])
    major = SelectField('Major', [Required()], choices=major_choices)
    grad_semester = SelectField('Graduation Semester', [Required()], choices=grad_semester_choices)
    grad_year = IntegerField('Graduation Year', [Required()])
    
