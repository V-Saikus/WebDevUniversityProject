from models import *
from config import *


def get_serializable_user(user):
    result = {
        'id': user.id,
        'first_name': user.first_name,
        'second_name': user.second_name,
        'birthday': user.birthday,
        'email': user.email,
        'phone_number': user.phone_number,
    }

    return result


@app.route('/user', methods=['POST'])
def create_user():
    first_name=request.form['first_name']
    second_name=request.form['second_name']
    birthday=request.form['birthday']
    email=request.form['email']
    phone_number=request.form['phone_number']
    password=request.form['password']
    email_check = User.query.filter_by(email=email).first()
    if email_check is not None:
        return jsonify({"msg": "User with such email already exists"}), 409
    tel_check = User.query.filter_by(phone_number=phone_number).first()
    if tel_check is not None:
        return jsonify({"msg": "User with such phone number already exists"}), 409
    db.session.add(User(first_name=first_name, second_name=second_name, birthday=birthday, email=email, phone_number=phone_number, password=generate_password_hash(password)))
    cursession['id'] = db.session.query(User).filter(User.first_name == request.form['first_name']).first().id
    db.session.commit()
    return jsonify({"Success": "User has been created"}), 201


@app.route('/user/<userId>', methods=['GET'])
def get_user(userId):
    try:
        int(userId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    current_user=User.query.filter_by(id=userId).first()
    if not current_user:
        return jsonify({"Error": "User not found"}), 404
    return jsonify(get_serializable_user(current_user)), 200


@app.route('/user/<userId>', methods=['PUT'])
@auth.login_required
def put_user(userId):
    user = User.query.filter_by(id=userId).first()
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    first_name=request.form['first_name']
    second_name=request.form['second_name']
    birthday=request.form['birthday']
    email=request.form['email']
    phone_number=request.form['phone_number']
    password=request.form['password']
    if not first_name and not second_name and not birthday and not email and not phone_number and not password:
        return jsonify(status='Invalid body supplied'), 404
    if first_name: User.query.filter_by(id=userId).update(dict(first_name=first_name))
    if second_name: User.query.filter_by(id=userId).update(dict(second_name=second_name))
    if birthday: User.query.filter_by(id=userId).update(dict(birthday=birthday))
    if email: User.query.filter_by(id=userId).update(dict(email=email))
    if phone_number: User.query.filter_by(id=userId).update(dict(phone_number=phone_number))
    if password: User.query.filter_by(id=userId).update(dict(password=generate_password_hash(password)))
    db.session.commit()
    return jsonify(status='updated user'), 202
