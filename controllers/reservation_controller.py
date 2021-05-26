from models import *
from config import *
import datetime

def get_serializable_reservation(reservation):
    result = {
        'id': reservation.id,
        'start_time': str(reservation.start_time),
        'end_time': str(reservation.end_time),
        'user_id': reservation.user_id,
        'audience_id': reservation.audience_id,
    }

    return result


@app.route('/audience/reserve', methods=['POST'])
@auth.login_required
def create_reservation():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    start_time=request.json.get('start_time', None)
    end_time=request.json.get('end_time', None)
    creator_id = auth.current_user().id
    audience_id=request.json.get('audience_id', None)
    reservation_list=Reservation.query.filter_by(audience_id=audience_id).all()
    db.session.add(Reservation(start_time=start_time, end_time=end_time, user_id=creator_id, audience_id=audience_id))
    db.session.commit()
    return jsonify({"Success": "reserve has been created"}), 201


@app.route('/audience/reserve/<reservationId>', methods=['GET'])
def get_reserve(reservationId):
    try:
        int(reservationId)
    except ValueError:
        return jsonify({"Error": "Invalid Id supplied"}), 400
    audience=Reservation.query.filter_by(id=reservationId).first()
    if not audience:
        return jsonify({"Error": "Reservation not found"}), 404
    return jsonify(get_serializable_reservation(audience)), 200


@app.route('/reserve/<reservationId>', methods=['PUT'])
@auth.login_required
def put_reserve(reservationId):
    reserve = Reservation.query.filter_by(id=reservationId).first()
    if reserve is None:
        return jsonify({"Error": "Reservation not found"}), 404
    start_time=request.json.get('start_time', None)
    end_time=request.json.get('end_time', None)
    if not start_time and not end_time:
        return jsonify(status='Invalid body supplied'), 404
    if start_time: Reservation.query.filter_by(id=reservationId).update(dict(start_time=start_time))
    if end_time: Reservation.query.filter_by(id=reservationId).update(dict(end_time=end_time))
    db.session.commit()
    return jsonify(status='updated reservation'), 202

@app.route('/reserve/<reservationId>', methods=['DELETE'])
@auth.login_required
def delete_reserve(reservationId):
    reserve = Reservation.query.filter_by(id=reservationId).first()
    if reserve is None:
        return jsonify({"Error": "Reservation not found"}), 404
    db.session.delete(reserve)
    db.session.commit()
    return jsonify(status='deleted reservation'), 200
