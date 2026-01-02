import sys
from jinja2 import Template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():

    args = sys.argv
    args.pop(0)
    df = pd.read_csv('data (1).csv' , skipinitialspace=True)
    print(df.columns.tolist())
    
    if len(args) == 1:
        display_error()
        sys.exit()
    
    elif len(args) == 2 and args[0] == '-s':
        write(process_s_data(df , args[1]))
        
    elif len(args) == 2 and args[0] == '-c':
        write(process_c_data(df , args[1]))
        
        

def process_s_data(df , student_id):
    courses = df.loc[df['Student id'] == int(student_id)]
    
    if(len(courses) == 0):
        write(display_error)
        sys.exit()
    
    total_marks = courses['Marks'].sum()
    
    student_template = '''
        <!DOCTYPE html>
        <html lang = "en">
        <head>
            <meta charset="UTF-8">
            <title>STUDENT DETAILS</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Student id</th>
                    <th>Course id</th>
                    <th>Marks</th>
                </tr>
                
                {% for row in courses %}
                <tr>
                    <td>{{ row['Student id'] }}</td>
                    <td>{{ row['Course id'] }}</td>
                    <td>{{ row['Marks'] }}</td>
                </tr>
                {% endfor %}
                <tr>
                    <td colspan="2">Total Marks</td>
                    <td> {{total_marks}}</td>
                </tr>
                
            </table>
        </body>
        
        </html>
        
    
    '''
    
    template = Template(student_template)
    content = template.render(courses=courses.to_dict(orient='records') , total_marks=total_marks)
    
    return content

def process_c_data(df , course_id):
    courses = df.loc[df['Course id'] == int(course_id)]
    
    if(len(courses) == 0):
        write(display_error)
        sys.exit()
    
    max_marks = courses['Marks'].max()
    average_marks = courses['Marks'].mean()
    make_plot(courses)
    
    course_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Course Details</title>
            
            <style>
                table{
                    border:1px solid;
                    
                }
                
                th , td {
                    border: 1px solid;
                }
                
            </style>
        
        </head>
        
        <body>
            <table>
                <tr>
                    <th>Average Marks</th>
                    <th>Maximum Marks</th>
                </tr>
                
                <tr>
                    <td>{{average_marks}}</td>
                    <td>{{max_marks}}</td>
                </tr>
            </table>
            
            <img src="plot.jpg"  alt="plot image">
            
            

            
        </body>
        </html>
        
    '''
    
    template = Template(course_template)
    content = template.render(max_marks = max_marks , average_marks = average_marks)
    return content
        
        

        
        
def display_error():
    error_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>something went wrong</title>
        </head>
        <body>
            <h1>INVALID INPUT</h1>
            <p>Something went wrong</p>
        </body>
        </html>
    
    '''
    template = Template(error_template)
    content = template.render()
    write(content)
    
def write(content):
    with open("output.html" , "w") as f:
        f.write(content)
    print("written to file")
    
def make_plot(data):
    marks = np.array(data['Marks'])
    plt.figure(figsize=(10,4))
    plt.hist(marks)
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('plot.jpg')
    plt.close()
        
        
if __name__ == "__main__":
    main()
        
