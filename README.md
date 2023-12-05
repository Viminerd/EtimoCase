# EtimoCase
REST-API for employee tracking

## Usage
- Download folder
- Server is being run on server.py. Call python server.py in terminal
- Send calls in browser <ip>:8080 or use localhost:8080 or use JSON via script.
- call python tests.py with various asserts to check the functionality of the endpoints


## Folder description 
- Folder **containers*: Has custom classes company and employee.
  - **company.py** contains functions and a dictionary of employees for handling.
  - **employee.py** contains information about each employee.
- Folder **templates*: Contains html pages for easy API calling in browser.
- Script **server.py**: Endpoints and server start.
- Script **tests.py**: Various calls and asserts to make sure the APIs does what is expected.
