import http.server
import socketserver
PORT = 8080
    
from flask import Flask, jsonify, render_template, request
import json

from containers import company, employee
def create_app(test_config=None ):
    app = Flask(__name__)
    company_handler = company.company_class(name="Etimo")
    name = "TESTNAME"
    email = "TEST"
    
    employee_to_add = employee.employee(name, email, "Not set")
    company_handler.add(employee_to_add)
    #GET: Go to home page 
    @app.route('/')
    @describe_route("/", "[GET] Homepage for server, lists available endpoints")
    def home_page(): 
        endpoints = [
        {'endpoint': getattr(app.view_functions[rule.endpoint], '_path'), 'description': getattr(app.view_functions[rule.endpoint], '_description')}
        for rule in app.url_map.iter_rules() if rule.endpoint != 'static'
        ]
        
        return render_template('home.html', endpoints=endpoints)

    #GET: List employees
    @app.route('/list_employees', methods=['GET'])
    @describe_route("/", "[GET] List of all employees")
    def employees_page(): 
        employee_list = company_handler.get_employees()
        employees = [{'name':employee.name,
        'email':employee.email, 
        'department':employee.department}           
        for key, employee in employee_list.items()
        ]
        
        return render_template('employee_list.html', employees=employees, number = company_handler.number_of_employees())


    #GET,POST: Add employee, page and command 
    add_employee = "/add_employee"
    @app.route(add_employee, methods=['GET','POST'])
    @describe_route(add_employee, "[GET] Takes you to employee add page, [POST] add a employee to the company, args-(name, email, department)")
    def add_employee_form():
        if request.method == 'GET':
            return render_template('add_employee_form.html')
        if request.method == 'POST':
            data = request.json
            name = parse_name(data['name'])
            email = delete_whitespaces(data['email'].lower())
            if 'department' in data:
                dep = delete_whitespaces(data['department'])
                if dep == "" or dep == None:
                    department = "Not set"
                else:
                    department = dep
            else:
                department = "Not set"
            if not company_handler.email_occupied(email):
                employee_to_add = employee.employee(name, email, department)
                company_handler.add(employee_to_add)
            else: 
                pass
                #send error message
        return render_template('add_employee_form.html')
    
    
    #GET,POST: delete employee. Page and command
    delete_employee = "/delete_employee"
    @app.route(delete_employee, methods=['GET','POST'])
    @describe_route(delete_employee, "[GET] Takes you to employee delete page. [POST] delete employee by enter email as arg.")
    def delete_employee():
        if request.method == 'GET':
            return render_template('delete_employee_form.html')
        if request.method == 'POST':
            data = request.json
            email = data['email'].lower()
            employees = company_handler.get_employees()
            if email in employees:
                company_handler.delete(employees[email])
            else: 
                pass
                #send error message
        return render_template('delete_employee_form.html')
    
    
    
    return app

#add a rule attribute on path for html display
def describe_route(path,description):
    def decorator(func):
        setattr(func, '_description', description)
        setattr(func, "_path", path)
        return func

    return decorator

def delete_whitespaces(string):
    while len(string)>0 and string[-1]==" ":
        string = string[0:len(string)-1]
        
    while len(string)>0 and string[0]==" ":
        string = string[1:len(string)]
    return string

def parse_name(string):
    string = delete_whitespaces(string)
    return string.title()


APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=PORT, debug=False)
  