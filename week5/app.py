from flask import Flask, request , render_template , redirect , url_for
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
        
@app.route('/student/create' , methods=['GET' , 'POST'])
def create_student():
    if request.method == "GET":
        return render_template("create_student.html")
    elif request.method=="POST":
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')
        
        existing_student = Student.query.filter_by(roll_number = roll_number).first()
        if existing_student:
            return render_template('existing_student.html')
        else:
            new_student = Student(roll_number=roll_number , first_name = first_name , last_name = last_name)
            db.session.add(new_student)
            db.session.commit()
            added_student = Student.query.filter_by(roll_number = roll_number).first()
            for course_name in courses:
                course = Course.query.filter_by(course_name = course_name).first()
                enrollment = Enrollments(estudent_id=added_student.student_id , ecourse_id = course.course_id)
                db.session.add(enrollment)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        return render_template('error.html')
    
    
@app.route('/student/<int:student_id>/update' , methods=["GET" ,"POST"])
def update_student(student_id):
    if request.method == "GET":
        student = Student.query.filter_by(student_id = student_id)
        return render_template('update_student.html' , student=student)
    elif request.method == "POST":
        student = Student.query.filter_by(student_id = student_id)
        student.roll_number = request.form['roll']
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        courses = request.form.getlist('courses')
        
        Enrollments.query.filter_by(estudent_id = student_id).delete()
        
        for course in courses:
            course_details = Course.query.filter_by(course_name = course)
            enrollment = Enrollments(estudent_id = student_id , ecourse_id = course_details.course_id)
            db.session.add(enrollment)
        db.session.commit()
        
        return redirect(url_for('home'))
    else:
        return render_template('error.html')
    
    
@app.route('/student/<int:student_id>/delete' , method=['GET'])
def delete_student(student_id):
    if request.method == "GET":
        student = Student.query.filter_by(student_id = student_id).first()
        db.session.delete(student)
        db.session.commt()
        Enrollments.query.filter_by(estudent_id = student_id).delete()
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('error.html')
    
    
@app.route('/student/<int:student_id' , methods=['GET'])
def view_student(student_id):
    if request.method == "GET":
        student = Student.query.filter_by(student_id = student_id).first()
        enrollments = Enrollments.query.filter_by(student_id = student_id).all()
        courses = []
        for enrollment in enrollments:
            course = Course.query.filter_by(course_id = enrollment.course_id).first()
            courses.append(course)
        
        return render_template('view_student.html' , student=student , courses = courses)
        
        

            

if __name__ == "__main__":
    app.run(debug=True)
    