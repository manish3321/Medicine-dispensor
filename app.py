from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for
import pymysql
import base64
import os
from datetime import datetime
from flask import jsonify




app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key


# MySQL configuration
connection = pymysql.connect(
    host='s783.bom1.mysecurecloudhost.com',  # e.g., 'localhost'
    user='evoqedco_medicine_dispenser',
    password='Manish123$',
    db='evoqedco_medicine_dispenser',
)

@app.route('/add-user', methods=['POST'])
def add_user():
    UserID = request.form['addUserId']
    patient_name = request.form['addPatientName']
    patient_age = request.form['addPatientage']
    rfid_tag = request.form['addUserRFID']
    image_data = request.form['addUserFace']

    # Extract the base64 image data
    if image_data.startswith('data:image/png;base64,'):
        image_data = image_data.replace('data:image/png;base64,', '')
        image_data = base64.b64decode(image_data)

         # Set the directory path to save the image
        directory = 'path/to/save/'  # Replace with your actual directory path
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist

        file_path = os.path.join(directory, 'user_image.png')  # Use os.path.join for better compatibility
        with open(file_path, 'wb') as f:
            f.write(image_data)


      # Connect to the database and insert the user details
    connection = pymysql.connect(

    host='s783.bom1.mysecurecloudhost.com',  # e.g., 'localhost'
    user='evoqedco_medicine_dispenser',
    password='Manish123$',
    db='evoqedco_medicine_dispenser',)

    with connection.cursor() as cursor:
        sql = "INSERT INTO patients (id, patient_name, patient_age, captured_image, RFID , timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (UserID, patient_name, patient_age, 'user_image.png', rfid_tag, datetime.now()))  # Save only the filename
    connection.commit()
    connection.close()



    # Instead of returning JSON, return a response to trigger a pop-up
    return redirect(url_for('dashboard', success='1'))







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
