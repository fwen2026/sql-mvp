import mysql.connector
import pandas as pd
from flask import Flask, redirect, request, url_for
import statistics

#In[1]
# Connects (establishes one) to the server. The actual root password is on here.

sql_connector = mysql.connector.connect(host='localhost',
                        database='submission_data',
                        user='root',
                        password='Technoblade!1')


cursor = sql_connector.cursor()


# These are all just methods to calculate values.
def add_row(data_list):
    try:
        query = "INSERT INTO data (name, a_sub, b_sub) VALUES (%s, %s, %s)"
        cursor.execute(query, data_list)
        sql_connector.commit() # This makes changes permanent
    except mysql.connector.errors.ProgrammingError:
        return "Row execution failed."


def calculate_percentage(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM data WHERE name =" + item)
    data_list = cursor.fetchall()
    total = 0.0
    sum = 0.0
    for element in data_list:
        total += 1.0
        sum += element[0]
    return (sum / total) * 100

def calculate_stdv(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM data WHERE name =" + item)
    data_list = cursor.fetchall()
    data_in_listform = []
    for element in data_list:
        data_in_listform.append(element[0])
    return statistics.stdev(data_in_listform)

def calculate_average(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM data WHERE name =" + item)
    data_list = cursor.fetchall()
    data_in_listform = []
    for element in data_list:
        data_in_listform.append(element[0])
    return statistics.mean(data_in_listform)


# In[2]
# This entire is where the functions are called.
app = Flask(__name__)


# Publishes data to the interface.
@app.route('/submission/')
def submission():
    data = request.args.get('data')
    return 'Percentage of a-submissions for this user is %s' % data + '%'


# Fetches data, calculates values.
@app.route('/index.html',methods = ['POST'])
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
    return redirect(url_for('submission', data=calculate_percentage('a_sub', "'" + submission_name + "'")))


if __name__ == '__main__':
    app.run(debug = True)