from flask import Flask, jsonify, render_template, request
import requests

url = "http://localhost:8080"
headers = {"Content-Type": "application/json"}

#Clear company
password = {'password':"Admin_password"}
r = requests.put(url+"/reset_company", json=password)
assert r.status_code==200

##Addition testing##
#Faulty add
employee_data = {
    'name' : "Viktor",
    'email' : "EMAIL",
    'department' : "department"
}
r = requests.post(url+"/add_employee", json=employee_data)
assert r.status_code == 400
r = requests.get(url+"/list_employees", headers=headers)
# Assert amount of employees = 0
assert len(r.json()) == 0

#Correct add, assert name and email formatting
employee_data = {
    'name' : "bRiTt-mARIE karlsson",
    'email' : "KARLSSON@gmail.com",
    'department' : ""
}
r = requests.post(url+"/add_employee", json=employee_data)
assert r.status_code == 200
r = requests.get(url+"/list_employees", headers=headers)
assert r.json()[0]['name'] != "bRiTt-mARIE karlsson"
assert r.json()[0]['name'] == "Britt-Marie Karlsson"
assert r.json()[0]['email'] == "karlsson@gmail.com"

#Assert adding 2 people with same name and different email
employee_data = {
    'name' : "Viktor Mineur",
    'email' : "email1@gmail.com",
    'department' : "  "
}
r = requests.post(url+"/add_employee", json=employee_data)
assert r.status_code == 200
employee_data['email'] = "email2@gmail.com"
r = requests.post(url+"/add_employee", json=employee_data)
assert r.status_code == 200
r = requests.get(url+"/list_employees", headers=headers)
assert len(r.json()) == 3
#Assert error adding same email
employee_data['name'] = "Johan Eriksson"
r = requests.post(url+"/add_employee", json=employee_data)
assert r.status_code == 400


##Deletion##
#Assert email deletion isn't case sensitive
r = requests.post(url+"/delete_employee", json={'email':"KArLssOn@gmail.com"})
assert r.status_code == 200

#Assert previously deleted employee can't be deleted again
r = requests.post(url+"/delete_employee", json={'email':"KArLssOn@gmail.com"})
assert r.status_code == 400

#Assert error when trying to delete employee non existing
r = requests.post(url+"/delete_employee", json={'email':"whatever@outlook.com"})
assert r.status_code == 400


r = requests.get(url+"/list_employees", headers=headers)
assert r.status_code == 200
print(r.json())






