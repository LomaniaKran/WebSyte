from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db

app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app2)
app2.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app2)
login_manager.login_view = 'authNew'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app2.route('/authNew', methods=['GET', 'POST'])
def authNew():
    if current_user.is_authenticated:
        return redirect(url_for('authNew'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profil'))
        else:
            flash('Invalid username or password')
    return render_template('authNew.html')

@app2.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('authNew'))
    return render_template('registration.html')

@app2.route('/profil', methods=['GET', 'POST'])
def profil():
    if current_user.is_authenticated:
        if request.method == 'GET':
            return render_template('profil.html', user=current_user)
        
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            user = User.query.filter_by(id=current_user.get_id()).first()
            user.email = email
            user.username = username
            db.session.commit()  
            return redirect(url_for('profil'))
     
    else:
        return redirect(url_for('authNew'))

@app2.route('/index')
def index():
    return render_template('index.html')

@app2.route('/motivation')
def motivation():
    return render_template('motivation.html')

@app2.route('/success')
def success():
    return render_template('success.html')

@app2.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authNew'))

if __name__ == '__main__':
    app2.run(host="0.0.0.0")