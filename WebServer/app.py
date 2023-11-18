from flask import Flask

from users import users_api
from friends import friends_api
from transactions import transactions_api

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db.init_app(app)
app.register_blueprint(users_api, url_prefix="/users")
app.register_blueprint(friends_api, url_prefix="/friends")
app.register_blueprint(transactions_api, url_prefix="/transactions")


"""
db_created = False


@app.before_request
def create_tables():
    global db_created
    if not db_created:
        db.create_all()
        db_created = True
"""


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
