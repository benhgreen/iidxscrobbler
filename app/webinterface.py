from flask import Flask, render_template, redirect, flash
app = Flask(__name__)
app.config.from_object('config')
from forms import SignupForm

@app.route('/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
    	flash('Registration successful.')
    	return redirect('/')
    return render_template('base.html', 
                           title='Sign Up',
                           form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()