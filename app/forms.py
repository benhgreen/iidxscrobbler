from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Regexp
from usermanager import *

class SignupForm(Form):
	userid = StringField('userid', validators=[DataRequired(), Regexp('^[0-9]{4}-[0-9]{4}$', message='Invalid network ID.')])
	network = SelectField('network', choices=[('ps', 'CS'), ('pw', 'AC')], validators=[DataRequired()])
	lastfmuser = StringField('lastfmuser', validators=[DataRequired()])

	def validate(self):
		if not Form.validate(self):
			return False

		if checkExistingUser(self.userid.data.replace(" ", ""), self.network.data):
			self.userid.errors.append("This ID is already subscribed. Please try another.")
			return False

		createUser(self.userid.data.replace(" ", ""), self.network.data, self.lastfmuser.data)
		return True

	def lfmURLGen(self):
		network = pylast.get_lastfm_network(os.environ.get('LFM_API'), os.environ.get('LFM_SECRET'))
		sg = pylast.SessionKeyGenerator(network)
		url = sg.get_web_auth_url()
		getDatabase().users.update(
		{'userid': self.userid.data, 'network': self.network.data},
		{
			'$set':{
					'lfm_url': url
			}
		})
		return url