from app import app , db , Course

with app.app_context():
    db.create_all()
    
    courses = [
        
        Course(course_code="CSE01" , course_name="MAD1" , course_description="Modern Application Development 1"),
        Course(course_code="CSE02" , course_name="DBMS" , course_description="Database Management Systems"),
        Course(course_code="CSE03" , course_name="PDSA" , course_description="Programming , Data Structures and Algorithms using Python"),
        Course(course_code="BST13" , course_name="BDM" , course_description="Business Data Management")
        
    ]
    
    db.session.bulk_save_objects(courses)
    db.session.commit()
    
    print("Data successfully entered in the table course")