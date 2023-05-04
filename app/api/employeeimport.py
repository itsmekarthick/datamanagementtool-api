import json
from flask import Blueprint, Response, request
from flask_cors import CORS
import pandas as pd
from app.api.employee import Employee
from app.api.validationresponse import ValidationResponse
from app.myencoder import MyEncoder

csv_file_path = "datafile/employee.csv"

employeeimport = Blueprint('employeeimport', __name__)
employeeimport.url_prefix = '/upload'
CORS(employeeimport)  # enable CORS for all routes

@employeeimport.route('/csv', methods=['POST'])
def post():
    file = request.files['file']
    data = pd.read_csv(file)
    if (data.empty):
        return json.dumps("CSV file is empty")

    employees = []
    employee_collections = []
    duplicate_employees = []
    non_duplicate_employees = []
    validation_messages = []
    
    # process the data
    map_records(data, employees)

    # Load the data from the CSV file
    df = pd.read_csv(csv_file_path)
   
    # Map the records from the target excel collection
    map_target_records(df, employee_collections)   

    # Find the duplicates records
    find_duplicates(employees, employee_collections, duplicate_employees, validation_messages)
    
    # Find the non duplicates records
    find_non_duplicates(employees, duplicate_employees, non_duplicate_employees)
    
    # Validate the uploaded records
    validate_records(non_duplicate_employees, validation_messages)
    
    return json.dumps(validation_messages, cls=MyEncoder)


def map_target_records(df, employee_collections):
    for _, row in df.iterrows():
        employee = Employee(
            firstname=row['First Name'],
            lastname=row['Last Name'],
            employeenumber=row['Employee Number'],
            mobilenumber=row['Phone Number'],
            email=row['Email']
        )
        employee_collections.append(employee)

def map_records(data, employees):
    for _, row in data.iterrows():
        employee = Employee(
            firstname=row['First Name'],
            lastname=row['Last Name'],
            employeenumber=row['Employee Number'],
            mobilenumber=row['Phone Number'],
            email=row['Email']
        )
        employees.append(employee)

def find_duplicates(employees, employee_collections, duplicate_employees, validation_messages):
    for emp in employees:
        for empcollection in employee_collections:
            if emp.employeenumber == empcollection.employeenumber or emp.email == empcollection.email or emp.mobilenumber == empcollection.mobilenumber:
                duplicate_employees.append(emp)
                validation_message = ValidationResponse(
                    firstname=emp.firstname,
                    lastname=emp.lastname,
                    employeenumber=emp.employeenumber,
                    mobilenumber=emp.mobilenumber,
                    email=emp.email,
                    responsetype='error',
                    message='Duplicate Employee Number or Email or Phone Number found'
                )
                validation_messages.append(validation_message)
                break
    
def find_non_duplicates(employees, duplicate_employees, non_duplicate_employees):
    for emp1 in employees:
        is_duplicate = False
        for emp2 in duplicate_employees:
            if emp1.employeenumber == emp2.employeenumber and emp1.mobilenumber == emp2.mobilenumber:
                is_duplicate = True
                break
        if not is_duplicate:
            non_duplicate_employees.append(emp1)
                    
# Validate the records
def validate_records(non_duplicate_employees, validation_messages):
    for emp in non_duplicate_employees:
        validation_message = ValidationResponse(
            firstname=emp.firstname,
            lastname=emp.lastname,
            employeenumber=emp.employeenumber,
            mobilenumber=emp.mobilenumber,
            email=emp.email,
            responsetype='success',
            message=''
        )

        # Check that Phonenumber is a valid integer
        try:
            int(emp.employeenumber)
        except ValueError:
            validation_message.responsetype = "error"
            validation_message.message = "Employee number must be a valid integer"
            
        # Check that Phonenumber is a valid integer
        try:
            int(emp.mobilenumber)
        except ValueError:
            validation_message.responsetype = "error"
            validation_message.message = "Phone Number must be a valid integer"

        # Check that email is a valid format
        if emp.email and '@' not in emp.email:
            validation_message.responsetype = "error"
            if validation_message.message:
                validation_message.message += ', '
            validation_message.message += 'Email must be a valid format'

        # Check that firstname is not too long
        if len(emp.firstname) > 20:
            validation_message.responsetype = "error"
            if validation_message.message:
                validation_message.message += ', '
            validation_message.message += 'First Name cannot be longer than 20 characters'
        
        # Check that lastname is not too long
        if len(emp.lastname) > 20:
            validation_message.responsetype = "error"
            if validation_message.message:
                validation_message.message += ', '
            validation_message.message += 'Last Name cannot be longer than 20 characters'
            
        # Check that email is not too long
        if len(emp.email) > 30:
            validation_message.responsetype = "error"
            if validation_message.message:
                validation_message.message += ', '
            validation_message.message += 'Email cannot be longer than 30 characters'
            
        # Check that name is not too long
        if len(emp.mobilenumber) > 10:
            validation_message.responsetype = "error"
            if validation_message.message:
                validation_message.message += ', '
            validation_message.message += 'Phone Number cannot be longer than 10 characters'

        validation_messages.append(validation_message)
