from flask import Flask
from models import User, db

app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app2)

if __name__ == '__main__':
    with app2.app_context():
        db.create_all()

    print('Корабли лавировали, лавировали..')