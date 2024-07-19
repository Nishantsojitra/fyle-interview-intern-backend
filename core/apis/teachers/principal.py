from flask import Blueprint, jsonify
from core.models import users


principal_blueprint = Blueprint('principal', __name__)

@principal_blueprint.route('/principal/teachers', methods=['GET'])
@authenticate_principal
def get_principal_teachers():
    teachers = users.query.filter_by(role='teacher').all()
    return jsonify({'data': [teacher.to_dict() for teacher in teachers]})

    
