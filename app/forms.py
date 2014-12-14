from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Regexp
from usermanager import *

class SignupForm(Form):
	userid = StringField('userid', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{4}$', message='Invalid network ID.')])
	network = SelectField('network', choices=[('ps', 'PS (Omnimix)'), ('pw', 'PW (Pendual)')], validators=[DataRequired()])
	lastfmuser = StringField('lastfmuser', validators=[DataRequired()])
	lastfmpwd = PasswordField('lastfmpwd', validators=[DataRequired()])

	def validate(self):
		if not Form.validate(self):
			return False

		if checkExistingUser(self.userid.data, self.network.data):
			self.userid.errors.append("This ID is already subscribed. Please try another.")
			return False
		
		if sessionKeyGen(self.lastfmuser.data, self.lastfmpwd.data) == "INVALID":
			self.lastfmuser.errors.append("These credentials don't work. Please try again")
			self.lastfmpwd.errors.append("These credentials don't work. Please try again")
			return False

		createUser(self.userid.data, self.network.data, self.lastfmuser.data, self.lastfmpwd.data)
		return True