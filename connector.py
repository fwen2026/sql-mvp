import mysql.connector
from flask import Flask, redirect, request, url_for, render_template
import statistics
import json



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
        print("Row implementation failed.")
        return
    
#TODO: Redundancy?
def modify_PerItem(data_list):
    try:
        cursor.execute("SELECT name FROM peritemdata") #TODO: ADD SQL FUNCTIONS
        names = cursor.fetchall()
        names_list = []
        for element in names:
            names_list.append(element)
        if data_list[0] in names_list:
            cursor.execute("UPDATE peritemdata")
            query = "SET name = %s, a_perc = %s, avg_sub = %s, stdv_sub = %s" 
            cursor.execute(query, data_list)
            sql_connector.commit()
        else:
            query = "INSERT INTO peritemdata (name, a_perc, avg_sub, stdv_sub) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, data_list)
        sql_connector.commit()
    except mysql.connector.errors.ProgrammingError:
        print("Update failed")
        return

#PerTeamData name: peritemdata
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

def get_names():
    cursor.execute("SELECT from")


# In[2]
#Flask
app = Flask(__name__)

# Publishes data to the interface.
@app.route('/submission/')
def submission():
    data = (request.args.get('perc'), request.args.get('stdv'), request.args.get('avg'))
    return render_template("interface.html", data=data)


@app.route('/get_data/<name>')
def load_data(name):
    raw_data_list = cursor.execute('SELECT a_perc, avg_sub, stdv_sub FROM peritemdata WHERE name=' + name)
    processed_data = []
    for element in raw_data_list:
        processed_data.append(element[0])
    return json.dumps(processed_data)
    #load into website placeholders


# Fetches data, calculates values, caches in PerItemData
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
    tuple_data = (submission_name,
                  calculate_percentage('a_sub', "'" + submission_name + "'"), 
                  calculate_stdv('integer_sub', "'" + submission_name + "'"),
                  calculate_average('integer_sub', "'" + submission_name + "'"))
    modify_PerItem(tuple_data)
    return render_template('index.html')

#TODO: add function to run when website loads. this should load prevoius data.

if __name__ == '__main__':
    app.run(debug = True)