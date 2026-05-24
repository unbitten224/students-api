def test_create_student(client):
    response = client.post(
        "/students",
        json={"nombre": "Juan", "apellido": "Pérez", "correo": "juan@email.com"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["nombre"] == "Juan"
    assert data["apellido"] == "Pérez"
    assert data["correo"] == "juan@email.com"
    assert "id" in data


def test_create_student_missing_field(client):
    response = client.post(
        "/students",
        json={"nombre": "Juan", "apellido": "Pérez"},
    )
    assert response.status_code == 400


def test_create_duplicate_email(client):
    client.post(
        "/students",
        json={"nombre": "Juan", "apellido": "Pérez", "correo": "juan@email.com"},
    )
    response = client.post(
        "/students",
        json={"nombre": "Ana", "apellido": "Gómez", "correo": "juan@email.com"},
    )
    assert response.status_code == 409


def test_list_students_empty(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert response.get_json() == []


def test_list_students(client):
    client.post(
        "/students",
        json={"nombre": "Juan", "apellido": "Pérez", "correo": "juan@email.com"},
    )
    response = client.get("/students")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Juan"


def test_get_student_by_id(client):
    create_resp = client.post(
        "/students",
        json={"nombre": "Juan", "apellido": "Pérez", "correo": "juan@email.com"},
    )
    student_id = create_resp.get_json()["id"]
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == student_id
    assert data["nombre"] == "Juan"


def test_get_student_not_found(client):
    response = client.get("/students/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0.0"}
