from extensions import db
from datetime import datetime


class Students(db.Model):
    __tablename__ = "Students"

    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    courses = db.relationship("Courses", secondary="Enrollments", back_populates="students")
    
    
    
class Courses(db.Model):
    __tablename__ = "Courses"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    students = db.relationship("Students",secondary="Enrollments",back_populates="courses")
    


class Enrollments(db.Model):
    __tablename__ = "Enrollments"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("Students.id"),nullable=False)
    course_id =  db.Column(db.Integer, db.ForeignKey("Courses.id"),nullable=False)
    enrolled_at = db.Column(db.DateTime, nullable=False)