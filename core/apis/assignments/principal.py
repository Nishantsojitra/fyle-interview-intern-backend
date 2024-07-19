from flask import Blueprint, jsonify, request
from core.models import assignments
from core import db

principal_blueprint = Blueprint('principal', __name__)

@principal_blueprint.route('/principal/assignments', methods=['GET'])
@authenticate_principal
def get_principal_assignments():
    assignments = assignments.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    return jsonify({'data': [assignment.to_dict() for assignment in assignments]})


assignment_blueprint = Blueprint('assignment', __name__)

@assignment_blueprint.route('/principal/assignments/grade', methods=['POST'])
@authenticate_principal
def grade_assignment_by_principal():
    data = request.get_json()
    assignment = assignment.query.get(data['id'])
    assignment.grade = data['grade']
    assignment.state = 'GRADED'
    db.session.commit()
    return jsonify({'data': assignment.to_dict()})
