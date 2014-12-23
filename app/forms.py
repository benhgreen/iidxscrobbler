from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Regexp
from usermanager import *

class SignupForm(Form):
	userid = StringField('userid', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{4}$', message='Invalid network ID.')])
	version = SelectField('version', choices=[('21', 'CS'), ('0', 'CS+'), ('22', 'AC')], validators=[DataRequired()])
	lastfmuser = StringField('lastfmuser', validators=[DataRequired()])

	def validate(self):
		if not Form.validate(self):
			return False

		if checkExistingUser(self.userid.data, self.version.data):
			self.userid.errors.append("This ID is already subscribed. Please try another.")
			return False

		if not checkUserValidity(self.userid.data, int(self.version.data)):
			self.userid.errors.append("Invalid userid.")
			return False

		createUser(self.userid.data.replace(" ", ""), self.version.data, self.lastfmuser.data)
		return True

	def lfmURLGen(self):
		network = pylast.get_lastfm_network(os.environ.get('LFM_APIKEY'), os.environ.get('LFM_SECRET'))
		sg = pylast.SessionKeyGenerator(network)
		url = sg.get_web_auth_url()
		getDatabase().users.update(
		{'userid': self.userid.data, 'version': self.version.data},
		{
			'$set':{
					'lfm_url': url
			}
		})
		return url