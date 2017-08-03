#!/usr/bin/python
import mysql.connector
import csv
import io
import sys
import datetime
import time

from flask import Flask, render_template, request
from csvvalidator  import CSVValidator


app = Flask(__name__, static_url_path='/static')

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

db = mysql.connector.connect(host='127.0.0.1', user='root', password='manumohan333', database='manu')


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
        cursor = db.cursor()
        try:
            #prepare a cursor object using cursor() method
            cursor.execute("select * from upload_history order by history")
            data = cursor.fetchall()
            return render_template("dbwrite.html",data=data)

        except:
            print("Error in Downloading Employee Data")

        finally:
            cursor.close()



@app.route('/download_data', methods=['GET', 'POST'])
def download_data():
    cursor = db.cursor()
    try:
        # prepare a cursor object using cursor() method
        cursor.execute("select * from employee")

        with open("M:\ASS\Manu\out.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)
            return "Data Downloaded Successfully !"

    except:
        return 'Error in Downloading Employee Data'

    finally:
        cursor.close()


def create_validator():
    return "File Present"
    print("in create_validator")
    file = request.files['inputcsvFile']
    stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
    csv_input = csv.reader(stream)

    validator = CSVValidator(csv_input)

    for row in csv_input:
        print(row[4])
        validator.add_value_check(row[4], int,
                                  'EX1', 'age must be an integer')
        return validator


@app.route('/handle_data', methods=['POST'])
def handle_data():
    cursor = db.cursor()
    try:
        file = request.files['inputcsvFile']

        if not file:
            return "No file"

        else:
            # create a validator
            return 'Me'
            create_validator()
            #problems = validator.validate()

            if problems:  # will not work with ivalidate() because it returns an iterator
                sys.exit(1)
            else:
                sys.exit(0)

        # if file and allowed_file(file.filename):
        stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_input = csv.reader(stream)

        for row in csv_input:
            if (row[2] == ""):
                return 'EMP ID of an employee cannot be blank! '

            else:
                now = datetime.now()
                tempDate = now.strftime('%Y-%m-%d %H:%M:%S')
                a = repr(tempDate)
                cursor.execute("insert into employee(`name`, `eid`,`company`,`age`,`sex`) values(%s, %s, %s, %s, %s)",row)
                cursor.execute("insert into upload_history(`history`) values (%s)" %a)
                return 'Data Saved to Database!'

    except:
        return 'Error occured in Uploading Data'


    finally:
        db.commit()
        cursor.close()



if __name__ == '__main__':
    app.run()
