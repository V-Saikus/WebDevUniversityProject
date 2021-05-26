from config import Base, db


class User(Base):
    id = db.Column('id', db.INTEGER, primary_key=True, unique=True)
    first_name = db.Column('first_name', db.VARCHAR(length=100), nullable=False)
    second_name = db.Column('second_name', db.VARCHAR(length=100))
    birthday = db.Column('birthday', db.VARCHAR(length=100))
    email = db.Column('email', db.VARCHAR(length=345), nullable=False)
    phone_number = db.Column('phone_number', db.VARCHAR(length=50), nullable=False)
    password = db.Column('password', db.VARCHAR(length=1234), nullable=False)


class Audience(Base):
    id = db.Column('id', db.INTEGER, primary_key=True, unique=True)
    name = db.Column('name', db.VARCHAR(length=100), nullable=False)
    user_id = db.Column('user_id', db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship("User", backref=db.backref("user"))
    price_for_hour = db.Column('price_for_hour', db.FLOAT, nullable=False)


class Reservation(Base):
    id = db.Column('id', db.INTEGER, primary_key=True, unique=True)
    start_time = db.Column('start_time', db.TIMESTAMP, nullable=False)
    end_time = db.Column('end_time', db.TIMESTAMP, nullable=False)
    user_id = db.Column('user_id', db.INTEGER, db.ForeignKey(User.id))
    user = db.relationship("User", backref=db.backref("user1"))
    audience_id = db.Column('audience_id', db.INTEGER, db.ForeignKey(Audience.id))
    audience = db.relationship("Audience", backref=db.backref("reservation"))



