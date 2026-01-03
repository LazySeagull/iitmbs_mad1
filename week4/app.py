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
        df = pd.read_csv('data (1).csv')
        
        if request.form.get('ID') == "student_id":
            student_id = request.form.get("id_value")
            courses = df.loc[df['student_id'] == int(student_id)]
            
            if len(courses == 0):
                return render_template('error.html')
            
            
            
    
    
if __name__ == "__main__":
    app.run(debug=False)