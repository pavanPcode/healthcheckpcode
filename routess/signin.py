from flask import Blueprint, render_template,url_for,redirect,session,request
from functools import wraps
from SignInCheck import verify

# Create a blueprint instance
auth = Blueprint('auth', __name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'crmemail1' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('signin.html')
        elif request.method == 'POST':

            email = request.form['email']
            plain_password = request.form['password']
            result = verify(email,plain_password)
            # if email == '123' and str(password) == '123':
            if result['status']:
                session['crmemail1'] = email
                session['name'] = result['name']
                session['role'] = result['role']
                # flash('Login successful!', 'success')#
                return redirect(url_for('Notifyapp.indexatt'))
            else:
                # flash('Invalid credentials', 'danger')
                return render_template('signin.html',ErrorMessage=result['message'])
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@auth.route('/logout')
def logout():
    session.pop('crmemail1', None)
    session.pop('name',None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))