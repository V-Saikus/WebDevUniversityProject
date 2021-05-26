from config import *
from controllers.user_controller import *
from controllers.audience_controller import *
from controllers.reservation_controller import *
from routes import *
from werkzeug.security import check_password_hash


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.password, password):
        return user

db.create_all()

if __name__ == '__main__':
    app.run()