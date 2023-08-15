from flask import Flask, render_template, request, redirect, url_for
from firebase_ops import get_data_from_firebase
import pyrebase



app = Flask(__name__, static_folder='static', static_url_path='/static')
# Initialize Firebase with your configuration

firebase_config = {
  "apiKey": "AIzaSyDENYFgKOaNZZKZsfzegkAGsjooFbYLtZg",
  "authDomain": "rfpdata2.firebaseapp.com",
  "databaseURL": "https://rfpdata2-default-rtdb.firebaseio.com/",
  "projectId": "rfpdata2",
  "storageBucket": "rfpdata2.appspot.com",
  "messagingSenderId": "448830409449",
  "appId": "1:448830409449:web:3997fcb518213c562bfe78"
};


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


@app.route('/')
def index():
    return "Render the Landing Page of rfpNEXT"



@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('user_login'))
        except Exception as e:
            return str(e)
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print (email, password)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return render_template('dashboard.html', user=user)
        except Exception as e:
            return str(e)
    return render_template('login.html')


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    #get data from firebase collections 'test'
    data = get_data_from_firebase()
    if request.method == 'POST':
        new_column = request.form['new_column']
        if new_column:
            data[new_column] = [""] * len(data.get(next(iter(data.values()))))
        else:
            for key in data:
                data[key].append("")
    return render_template('editor.html', data=data)



#@app.route('/dashboard', methods=['GET', 'POST'])
#def user_dashboard():


if __name__ == '__main__':
    app.run(debug=True)


