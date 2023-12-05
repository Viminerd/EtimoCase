import http.server
import socketserver
PORT = 8080
    
from flask import Flask, jsonify, render_template, request
import json

from containers import company, employee
def create_app(test_config=None ):
    app = Flask(__name__)
    company_handler = company.company_class(name="Etimo")
    
    #GET: Go to home page 
    @app.route('/')
    @describe_route("/", "[GET] HTML-Homepage, JSON-list of available endpoints")
    def home_page(): 
        endpoints = [
        {'endpoint': getattr(app.view_functions[rule.endpoint], '_path'), 'description': getattr(app.view_functions[rule.endpoint], '_description')}
        for rule in app.url_map.iter_rules() if rule.endpoint != 'static'
        ]
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'endpoints': endpoints})
        else:
            return render_template('home.html', endpoints=endpoints)

    #GET: List employees
    @app.route('/list_employees', methods=['GET'])
    @describe_route("/list_employees", "[GET] HTML:List of all employees. JSON:Nothing")
    def employees_page(): 
        employee_list = company_handler.get_employees()
        employees = [{'name':employee.name,
        'email':employee.email, 
        'department':employee.department}           
        for key, employee in employee_list.items()
        ]
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify(employees)
        else:
            return render_template('employee_list.html', employees=employees, number = company_handler.number_of_employees())


    #GET,POST: Add employee, page and command 
    add_employee = "/add_employee"
    @app.route(add_employee, methods=['GET','POST'])
    @describe_route(add_employee, "[GET] HTML:Takes you to employee add page, JSON:Nothing. [POST] add a employee to the company, args-(name, email, department)")
    def add_employee_form():
        if request.method == 'GET':
            if request.headers.get('Content-Type') ==       'application/json':
                 return jsonify({}), 204
            else:
                return render_template('add_employee_form.html')
        if request.method == 'POST':
            data = request.json
            name = parse_name(data['name'])
            email = delete_whitespaces(data['email'].lower())
            if email.find('@') == -1:
                print("Email: "+data['email']+" invalid.")
                return {"Error": "Email: "+data['email']+" invalid."}, 400
            
            if 'department' in data:
                dep = delete_whitespaces(data['department'])
                if dep == "" or dep == None:
                    department = "Not set"
                else:
                    department = dep
            else:
                department = "Not set"
                
            employee_to_add = employee.employee(name, email, department)
            if(company_handler.add(employee_to_add)):
                return {"Success": "Employee: "+name+" was added."}, 200
            else: 
                print("Email: "+data['email']+" already in use.")
                return {"Error": "Email: "+data['email']+" already in use."}, 400
    
    
    #GET,POST: delete employee. Page and command
    delete_employee = "/delete_employee"
    @app.route(delete_employee, methods=['GET','POST'])
    @describe_route(delete_employee, "[GET] HTML:Takes you to employee delete page, JSON:Nothing. [POST] delete employee by enter email as arg.")
    def delete_employee():
        employee_list = company_handler.get_employees()
        employees = [{'name':employee.name,
            'email':employee.email, 
            'department':employee.department}           
            for key, employee in employee_list.items()
            ]
        if request.method == 'GET':
            if request.headers.get('Content-Type') ==       'application/json':
                 return jsonify({}), 204
            else:
                return render_template('delete_employee_form.html', employees = employees)
        if request.method == 'POST':
            data = request.json
            email = data['email'].lower()
            employees = company_handler.get_employees()
            if email in employees:
                if(company_handler.delete(employees[email])):
                    return {"Success": "Employee with email: "+data['email']+" was deleted."}, 200
            else: 
                print("Employee with email: "+data['email']+" not found.")
                return {"Error": "Employee email not found"}, 400
        return render_template('delete_employee_form.html', employees = employees)
    
    
    #GET,POST: Resets company for script asserts
    reset = "/reset_company"
    @app.route(reset, methods=['PUT'])
    @describe_route(reset, "[PUT] Deletes all employees and resets company")
    def reset():
        data = request.json
        password = data['password']

        if(company_handler.reset(password)):
            return {"Success": "Company reset."}, 200
        else: 
            return {"Error": "Company not reset, check password"}, 400
    
    
    
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
  