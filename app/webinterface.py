from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask, render_template, redirect, flash
app = Flask(__name__)
app.config.from_object('config')
from forms import SignupForm
import os, pylast

@app.route('/', methods=['GET', 'POST'])
def signup():
		form = SignupForm()
		if form.validate_on_submit():
			network = pylast.get_lastfm_network(os.environ.get('LFM_API'), os.environ.get('LFM_SECRET'))
			sg = pylast.SessionKeyGenerator(network)
			url=sg.get_web_auth_url()
			createUser(self.userid.data.replace(" ", ""), self.network.data, self.lastfmuser.data, url)

			return redirect('url')
			
		return render_template('base.html', 
													 title='Sign Up',
													 form=form)

if __name__ == '__main__':
	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(5000)
	IOLoop.instance().start()