from flask import Flask , request , render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/',methods = ['GET' , 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        df = pd.read_csv('data (1).csv' , skipinitialspace=True)
        
        if request.form.get("ID") == "student_id":
            return student_data(df , request.form.get("id_value"))
        
        elif request.form.get("ID") == "course_id":
            return course_data(df , request.form.get("id_value"))
        else:
            return render_template('error.html')
        
        
def student_data(df , student_id):
    courses = df.loc[df['Student id'] == int(student_id)]
    
    if(len(courses) == 0):
        return render_template("error.html")
    
    total_marks = courses['Marks'].sum()
    
    return render_template("student_data.html" , courses=courses.to_dict(orient='records') , total_marks=total_marks)

def course_data(df , course_id):
    courses = df.loc[df['Course id'] == int(course_id)]
    
    if len(courses) == 0:
        return render_template('error.html')
    
    max_marks = courses['Marks'].max()
    avg_marks = courses['Marks'].mean()
    export_plot(courses['Marks'])
    
    return render_template("course_data.html" ,max_marks=max_marks , avg_marks=avg_marks)

def export_plot(marks):
    marks_array = np.array(marks)
    plt.figure(figsize=(10,4))
    plt.hist(marks_array)
    plt.title("Marks Histogram")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig('static/require_plot.png')
    plt.close()

if __name__ == "__main__":
    app.run(debug=True)