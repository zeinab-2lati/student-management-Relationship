from flask import Flask, request
from extensions import db
from services import (
    get_all_students,
    get_Students_by_id,
    add_Students,
    update_Students,
    delete_Students as delete_Students_service,
    add_courses,
    enroll_student_service,
    delete_course_student_service,
    get_student_courses_service,
    get_course_students_service,
    get_all_courses,
    get_course_by_id,
    email_exists
)
from flasgger import Swagger
from marshmallow import ValidationError
from schemas import StudentSchema


app = Flask(__name__)
student_schema = StudentSchema()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

Swagger(app)

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Flask connected to database!"


# ---------------- STUDENTS ----------------

@app.route("/students", methods=["POST"])
def add_new_Students():
    """
    Add a new student
    ---
    consumes:
      - application/json

    parameters:
      - in: body
        name: student
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            email:
              type: string
            age:
              type: integer

    responses:
      201:
        description: Student added successfully
    """

    data = request.json

    try:
        validated_data = student_schema.load(data)

    except ValidationError as error:
       if "email" in error.messages:
        message = "Invalid email"
       elif "age" in error.messages:
        message = "Invalid age"
       elif "first_name" in error.messages:
        message = "Invalid first_name"
       else:
        message = "Invalid data"

       return {
        "success": False,
        "message": message
       }, 400

    students = add_Students(validated_data)

    return {
        "message": "student added successfully",
        "id": students.id
    }, 201


@app.route("/students", methods=["GET"])
def get_students():
  
    """
    Get all students with filters
    ---
    parameters:
      - name: first_name
        in: query
        type: string
        required: false


      - name: last_name
        in: query
        type: string
        required: false


      - name: email
        in: query
        type: string
  
        required: false


      - name: age
        in: query
        type: integer
        required: false


    responses:
      200:
        description: List of students
    """

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    email = request.args.get("email")
    age = request.args.get("age")

    students = get_all_students(
        first_name,
        last_name,
        email,
        age
    )

    return students


@app.route("/students/<int:id>", methods=["GET"])
def get_students_by_id(id):
    """
    Get a student by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true


    responses:
      200:
        description: Student found successfully

      404:
        description: Student not found
    """

    students = get_Students_by_id(id)

    if students is None:
        return {"message": "student not found"}, 404

    return {
        "id": students.id,
        "first_name": students.first_name,
        "last_name": students.last_name,
        "email": students.email,
        "age": students.age
    }, 200


@app.route("/students/<int:id>", methods=["PUT"])
def update_new_students(id):
  
    """
    Update a student
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true


      - in: body
        name: student
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            email:
              type: string
            age:
              type: integer

    responses:
      200:
        description: Student updated successfully

      400:
        description: Validation error

      404:
        description: Student not found
    """

    data = request.json

    try:
        validated_data = student_schema.load(data)

    except ValidationError as error:
        if "email" in error.messages:
            message = "Invalid email"
        elif "age" in error.messages:
            message = "Invalid age"
        elif "first_name" in error.messages:
            message = "Invalid first_name"
        else:
            message = "Invalid data"

        return {
            "success": False,
            "message": message
        }, 400

    if email_exists(validated_data["email"], exclude_id=id):
        return {
            "success": False,
            "message": "Email already exists"
        }, 400

    students = update_Students(id, validated_data)

    if students is None:
        return {
            "message": "student not found"
        }, 404

    return {
        "message": "student updated successfully"
    }, 200



@app.route("/students/<int:id>", methods=["DELETE"])
def delet_student(id):
    """
    Delete a student
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        
    responses:
      200:
        description: Student deleted successfully

      404:
        description: Student not found
    """

    students = delete_Students_service(id)

    if students is None:
        return {"message": "student not found"}, 404

    return {
        "message": "student deleted successfully"
    }, 200


# ---------------- COURSES ----------------

@app.route("/courses", methods=["POST"])
def add_new_courses():
    """
    Add a new course
    ---
    consumes:
      - application/json

    parameters:
      - in: body
        name: course
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            price:
              type: integer

    responses:
      201:
        description: Course added successfully
    """

    data = request.json
    courses = add_courses(data)

    return {
        "message": "course added successfully",
        "id": courses.id
    }, 201


@app.route("/courses", methods=["GET"])
def get_courses():
    """
    Get all courses
    ---
    responses:
      200:
        description: List of courses
    """

    courses = get_all_courses()

    return courses, 200


@app.route("/courses/<int:id>", methods=["GET"])
def get_course(id):
  
    """
    Get a course by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true


    responses:
      200:
        description: Course found successfully

      404:
        description: Course not found
    """

    course = get_course_by_id(id)

    if course is None:
        return {"message": "course not found"}, 404

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "price": course.price
    }, 200


@app.route("/courses/<int:course_id>/enroll", methods=["POST"])
def enroll_student(course_id):
    """
    Enroll a student in a course
    ---
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true


      - in: body
        name: enrollment
        required: true
        schema:
          type: object
          properties:
            student_id:
              type: integer

    responses:
      201:
        description: Student enrolled successfully

      404:
        description: Student or course not found
    """

    data = request.json
    student_id = data["student_id"]

    enrollment = enroll_student_service(
        course_id,
        student_id
    )

    if enrollment is None:
        return {
            "message": "student or course not found"
        }, 404

    return {
        "message": "student enrolled successfully",
        "id": enrollment.id
    }, 201


@app.route(
    "/courses/<int:course_id>/students/<int:student_id>",
    methods=["DELETE"]
)
def delete_course_student(course_id, student_id):
    """
    Remove a student from a course
    ---
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true

      - name: student_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Student removed from course successfully

      404:
        description: Enrollment not found
    """

    enrollment = delete_course_student_service(
        course_id,
        student_id
    )

    if enrollment is None:
        return {"message": "enrollment not found"}, 404

    return {
        "message": "student removed from course successfully"
    }, 200


@app.route("/students/<int:id>/courses", methods=["GET"])
def get_student_courses(id):
    """
    Get courses of a student
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true


    responses:
      200:
        description: List of courses

      404:
        description: Student not found
    """

    courses = get_student_courses_service(id)

    if courses is None:
        return {"message": "student not found"}, 404

    return courses, 200


@app.route("/courses/<int:id>/students", methods=["GET"])
def get_course_students(id):
    """
    Get students of a course
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true


    responses:
      200:
        description: List of students

      404:
        description: Course not found
    """

    students = get_course_students_service(id)

    if students is None:
        return {"message": "course not found"}, 404

    return students, 200


if __name__ == "__main__":
    app.run(debug=True)