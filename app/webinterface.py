from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask, render_template, redirect, flash
from forms import SignupForm
app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		return redirect(form.lfmURLGen())
		
	return render_template('base.html', 
		title='Sign Up',
		form=form)

if __name__ == '__main__':
	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(5000)
	IOLoop.instance().start()