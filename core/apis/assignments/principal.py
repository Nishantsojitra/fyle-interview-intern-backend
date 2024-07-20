from flask import Blueprint, request, jsonify
from core.models.assignments import Assignment
from core.libs.exceptions import AssignmentNotFoundException
from core.libs.exceptions import AssignmentNotFoundException

assignment_blueprint = Blueprint('assignment_blueprint', __name__)
principal_blueprint = Blueprint('principal_blueprint', __name__)

@principal_blueprint.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    
    # Fetch all assignments with state 'SUBMITTED' or 'GRADED'
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    
    # Serialize assignments
    assignments_data = [assignment.to_dict() for assignment in assignments]
    
    return jsonify({"data": assignments_data})

@assignment_blueprint.route('/principal/assignments/grade', methods=['POST'])
def grade_assignment_by_principal():
    data = request.get_json()
    
    assignment_id = data.get('id')
    grade = data.get('grade')
    
    # Fetch assignment
    assignment = Assignment.query.get(assignment_id)
    
    if not assignment:
        raise AssignmentNotFoundException(f"Assignment with id {assignment_id} not found.")
    
    if assignment.state != 'SUBMITTED':
        return jsonify({"error": "Assignment is not in a state that can be graded."}), 400
    
    # Set the grade
    assignment.grade = grade
    assignment.state = 'GRADED'
    
    # Commit changes
    db.session.commit()
    
    return jsonify({"data": assignment.to_dict()})

def principal_headers():
    return {'X-Principal': '{"principal_id": 1, "user_id": 5}'}    