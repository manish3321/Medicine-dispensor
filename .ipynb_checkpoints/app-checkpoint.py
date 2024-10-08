from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key

# Mock user data for authentication (Replace this with a database in a real application)
users = {
    'admin': 'password123'  # username: password
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['authenticated'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials. Please try again.', 401

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
