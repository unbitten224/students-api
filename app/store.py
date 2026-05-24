import uuid

_students = {}


def get_all():
    return list(_students.values())


def get_by_id(student_id):
    return _students.get(student_id)


def create(nombre, apellido, correo):
    student_id = str(uuid.uuid4())
    student = {
        "id": student_id,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
    }
    _students[student_id] = student
    return student


def email_exists(correo):
    return any(s["correo"] == correo for s in _students.values())


def clear():
    _students.clear()
