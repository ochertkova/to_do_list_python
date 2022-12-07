from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", boolean=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            pass
        else:
            pass
        # add user to database
    return render_template('sign_up.html')
