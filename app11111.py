from functools import wraps
from flask import Flask, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Mock user data (for demonstration)
users = {
    'pavan': '123',
    'jane': 'pass456',
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/')
@login_required
def index():
    return 'success'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)
