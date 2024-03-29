from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=5,max=50)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message="Passwords do not match")])
    confirm = PasswordField('Confirm Password',[validators.DataRequired()])

class SendMoneyForm(Form):
    username = StringField('Username',[validators.Length(min=5,max=50)])
    amount = StringField('Amount',[validators.Length(min=1,max=50)])

class BuyMoneyForm(Form):
    amount = StringField('Amount',[validators.Length(min=1,max=50)])
