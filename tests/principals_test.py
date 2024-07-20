from core.models.assignments import AssignmentStateEnum, GradeEnum

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_principal_can_grade_assignment(client, principal_headers):
    response = client.post('/principal/assignments/grade', headers=principal_headers, json={'id': 1, 'grade': 'A'})
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['id'] == 1
    assert data['grade'] == 'A'
    assert data['state'] == 'GRADED'



# @pytest.fixture
# def principal_headers():
#     return {'Authorization': 'Bearer principal_token'}

# class PrincipalsTestCase:
#     @classmethod
#     def setUpClass(cls):
#         cls.app = create_app('testing')
#         cls.client = cls.app.test_client()
#         cls.app_context = cls.app.app_context()
#         cls.app_context.push()
#         db.create_all()

#     @classmethod
#     def tearDownClass(cls):
#         db.session.remove()
#         db.drop_all()
#         cls.app_context.pop()

#     def test_get_assignments(self, principal_headers):
#         response = self.client.get('/api/principal/assignments', headers=principal_headers)
#         assert response.status_code == 200

#     def test_grade_assignment_draft_assignment(self):
#         assignment_id = 1
#         response = self.client.post('/api/principal/assignments/grade', json={'id': assignment_id, 'grade': 'A'})
#         assert response.status_code == 200
