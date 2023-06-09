import mysql.connector
import pandas as pd
from flask import Flask, redirect, request, url_for

#In[1]

# Connects to the server. The actual root password is on here.
sql_connector = mysql.connector.connect(host='localhost',
                        database='submission_data',
                        user='root',
                        password='Technoblade!1') # This is the actual password, so keep it secret.


cursor = sql_connector.cursor()

# These are all just methods to calculate values.
# THIS WORKS
def add_row(data_list):
    try:
        cursor.execute("INSERT INTO data VALUES " + str(data_list))
        sql_connector.commit() # This makes changes permanent
    except mysql.connector.errors.ProgrammingError:
        return "Row execution failed."

# THIS WORKS
def calculate_percentage(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM data WHERE name =" + item)
    data_list = cursor.fetchall()
    total = 0.0
    sum = 0.0
    for element in data_list:
        total += 1.0
        sum += element[0]
    return sum / total

#In[2]

#This is where the functions are called.
app = Flask(__name__)

# THIS WORKS.
# Publishes data to the interface.
@app.route('/submission/')
def submission():
    data = request.args.get('data')
    return 'Percentage of %s' % data


# THIS MAYBE WORKS???
# Fetches data, calculates values.
@app.route('/index',methods = ['POST'])
def calculate_data_points():
    submission_name = request.form['name']
    submission_ab = request.form['form-tester']
    if submission_ab == 'A':
        a_sub = 1
        b_sub = 0
    else:
        a_sub = 0
        b_sub = 1
    add_row((submission_name, a_sub, b_sub))
    return redirect(url_for('submission', data=calculate_percentage(submission_name, 'a_sub')))

if __name__ == '__main__':
    app.run(debug = True)

#In[3]

# def calculate_average(data_point, item):
# def calculate_stdv(data_point, item):
# These are good to have, but they aren't really nessecary for a full MVP in this case. 
# Remember when calling add_row to put '' around strings.

#In[4]