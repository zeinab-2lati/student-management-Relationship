from models import Students, Courses, Enrollments
from datetime import datetime
from extensions import db


def get_all_students(first_name=None, last_name=None, email=None, age=None):
    query = Students.query

    if first_name:
        query = query.filter_by(first_name=first_name)

    if last_name:
        query = query.filter_by(last_name=last_name)

    if email:
        query = query.filter_by(email=email)

    if age:
        query = query.filter_by(age=age)

    students = query.all()

    students_list = []

    for student in students:
        students_list.append({
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "age": student.age
        })

    return students_list

def get_Students_by_id(id):
    return Students.query.get(id)


def add_Students(data):
    students = Students(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        age=data["age"]
    )

    db.session.add(students)
    db.session.commit()

    return students

def update_Students(id, data):
    students = Students.query.get(id)
    
    if students is None:
        return None

    students.first_name = data["first_name"]
    students.last_name = data["last_name"]
    students.email = data["email"]
    students.age = data["age"]

    db.session.commit()

    return students

def delete_Students(id):
    students = Students.query.get(id)
    if students is None:
        return None
    
    db.session.delete(students)
    db.session.commit()
    return students
    
def add_courses(data):
    courses = Courses(
        title=data["title"],
        description=data["description"],
        price=data["price"]
    )

    db.session.add(courses)
    db.session.commit()

    return courses

def get_all_courses():

    courses = Courses.query.all()

    courses_list = []

    for course in courses:
        courses_list.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "price": course.price
        })

    return courses_list

def get_course_by_id(id):
    course = Courses.query.get(id)

    if course is None:
        return None

    return course

def enroll_student_service(course_id, student_id):
    student = Students.query.get(student_id)
    course = Courses.query.get(course_id)

    if student is None or course is None:
        return None

    enrollment = Enrollments(
        student_id=student_id,
        course_id=course_id,
        enrolled_at=datetime.now()
    )

    db.session.add(enrollment)
    db.session.commit()

    return enrollment

def delete_course_student_service(course_id, student_id): 
    enrollment = Enrollments.query.filter_by( course_id=course_id, student_id=student_id ).first() 
    if enrollment is None:
        return None 
    db.session.delete(enrollment) 
    db.session.commit() 
    return enrollment

def get_student_courses_service(student_id):
    student = Students.query.get(student_id)

    if student is None:
        return None

    courses_list = []

    for course in student.courses:
        courses_list.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "price": course.price
        })

    return courses_list

def get_course_students_service(course_id):
    course = Courses.query.get(course_id)

    if course is None:
        return None

    students_list = []

    for student in course.students:
        students_list.append({
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "age": student.age
        })

    return students_list