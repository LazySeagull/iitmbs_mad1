from flask import Flask, request , render_template 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer , primary_key = True , auto_increment=True)
    roll_number = db.Column(db.String , unique=True , nullable = False)
    first_name = db.Column(db.String , nullable = False)
    last_name = db.Column(db.String)
    
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer , primary_key=True , auto_increment=True)
    course_code = db.Column(db.String , unique=True , nullable = False)
    course_name = db.Column(db.String ,  nullable = False)
    course_description = db.Column(db.String)
    
class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer , primary_key = True , auto_increment=True)
    estudent_id = db.Column(db.Integer , db.ForeignKey("student.student_id") , nullable=False)
    ecourse_id = db.Column(db.Integer , db.ForeignKey("course.course_id") , nullable=False)
    
    
@app.route("/" , methods=['GET'])
def home():
    students = Student.query.all()
    if students:
        return render_template('index.html' , students=students)
    else:
        return render_template('index_no_student.html')
        



if __name__ == "__main__":
    app.run(debug=True)
    