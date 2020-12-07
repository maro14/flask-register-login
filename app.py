from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/', methods=['GET', 'POST'])
def homepage():
    if not session.get('logged_in'):
        return render_template('main.html')
    else:
        if request.method == 'POST':
            username = request.form['username']
            return render_template('base.html', data=username)
        return render_template('index.html')



@app.route('/register/', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        new_user = User(
            username = request.form['username'],
            password = request.form['password']
        )

        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else :
        name = request.form['name']
        passw = request.form['password']

        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
            else:
                return 'Error'
        except:
            return 'Error'
        


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))



if __name__ == "__main__":
    db.create_all()
    app.secret_key = '123'
    app.run(debug=True, host='localhost' )