import mysql.connector
from flask import Flask, redirect, request, url_for
import statistics
import os



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
        query = "INSERT INTO submissiondata (name, a_sub, b_sub, integer_sub) VALUES (%s, %s, %s, %s)" # No more SQL injections
        cursor.execute(query, data_list)
        sql_connector.commit() 
    except mysql.connector.errors.ProgrammingError:
        print("Row execution failed.")
        return


def calculate_percentage(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM submissiondata WHERE name =" + item) #TODO: Add sql percentages
    data_list = cursor.fetchall()
    total = 0.0
    sum = 0.0
    for element in data_list:
        total += 1.0
        sum += element[0]
    return (sum / total) * 100

def calculate_stdv(data_point, item):
    try:
        cursor.execute("SELECT " + data_point + " FROM submissiondata WHERE name =" + item)
        data_list = cursor.fetchall()
        data_in_listform = []
        for element in data_list:
            data_in_listform.append(element[0])
        return statistics.stdev(data_in_listform)
    except statistics.StatisticsError:
        return 0

def calculate_average(data_point, item):
    cursor.execute("SELECT " + data_point + " FROM submissiondata WHERE name =" + item) #TODO: ADD SQL FUNCTIONS
    data_list = cursor.fetchall()
    data_in_listform = []
    for element in data_list:
        data_in_listform.append(element[0])
    return statistics.mean(data_in_listform)


# In[2]
#Flask
app = Flask(__name__)


# Publishes data to the interface.
@app.route('/submission/')
def submission():
    data = (request.args.get('perc'), request.args.get('stdv'), request.args.get('avg'))
    return 'Stats for this user are: %s' % str(data)


# Fetches data, calculates values.
@app.route('/index.html',methods= ['GET', 'POST'])
def calculate_data_points():
    submission_name = request.form['name']
    submission_ab = request.form['form-tester']
    if submission_ab == 'A':
        a_sub = 1
        b_sub = 0
    else:
        a_sub = 0
        b_sub = 1
    submission_int = request.form['number']
    add_row((submission_name, a_sub, b_sub, submission_int))
    tuple_data = (calculate_percentage('a_sub', "'" + submission_name + "'"), 
                calculate_stdv('integer_sub', "'" + submission_name + "'"),
                calculate_average('integer_sub', "'" + submission_name + "'"))
    return redirect(url_for('submission', perc=tuple_data[0], stdv=tuple_data[1], avg=tuple_data[2]))


if __name__ == '__main__':
    app.run(debug = True)