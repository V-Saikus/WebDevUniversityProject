from models import *
from config import *


def get_serializable_audience(audience):
    result = {
        'id': audience.id,
        'name': audience.name,
        'price_for_hour': audience.price_for_hour,
        'user_id': audience.user_id,
    }

    return result


@app.route('/audience', methods=['POST'])
@auth.login_required
def create_audience():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    name=request.json.get('name', None)
    price_for_hour=request.json.get('price_for_hour', None)
    creator_id = auth.current_user().id
    db.session.add(Audience(name=name, price_for_hour=price_for_hour, user_id=creator_id))
    db.session.commit()
    return jsonify({"Success": "audience has been created"}), 201

@app.route('/audience', methods=['GET'])
def get_audiences():
    audiences = Audience.query.all()
    if len(audiences) == 0:
        return jsonify({"msg": "No schedules found"}), 404
    else:
        return jsonify([get_serializable_audience(var) for var in audiences]), 200

@app.route('/audience/<audienceId>', methods=['GET'])
def get_audience(audienceId):
    try:
        int(audienceId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    audience=Audience.query.filter_by(id=audienceId).first()
    if not audience:
        return jsonify({"Error": "Audience not found"}), 404
    return jsonify(get_serializable_audience(audience)), 200


@app.route('/audience/<audienceId>', methods=['PUT'])
@auth.login_required
def put_audience(audienceId):
    audience = Audience.query.filter_by(id=audienceId).first()
    if audience is None:
        return jsonify({"Error": "audience not found"}), 404
    name = request.json.get('name', None)
    price_for_hour = request.json.get('price_for_hour', None)
    if not name and not price_for_hour:
        return jsonify(status='Invalid body supplied'), 404
    if name: audience.query.filter_by(id=audienceId).update(dict(name=name))
    if price_for_hour: audience.query.filter_by(id=audienceId).update(dict(price_for_hour=price_for_hour))
    db.session.commit()
    return jsonify(status='updated audience'), 202
