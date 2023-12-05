# EtimoCase
REST-API for employee tracking

## Usage
- Download folder
- Assert flask is downloaded, can be downloaded in terminal with python3 -m pip install flask
- Server is being run on server.py. Run python server.py in terminal
- Send calls in browser with either \>ip\<:8080 or localhost:8080. You can also use a script with JSON type calls. 
- Run python tests.py with various asserts to check the functionality of the endpoints


## Folder description 
- Folder *containers*: Has custom classes company and employee.
  - **company.py** contains functions and a dictionary of employees for handling.
  - **employee.py** contains information about each employee.
- Folder *templates*: Contains html pages for easy API calling in browser.
- Script **server.py**: Endpoints and server start.
- Script **tests.py**: Various calls and asserts to make sure the APIs does what is expected.
