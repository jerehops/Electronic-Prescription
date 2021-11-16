
# Electronic Prescription System
*An online platform for medical prescriptions.*
## Project Setup
**Prerequisites**
- Python3
- [pip](https://pip.pypa.io/en/stable/installation/)
- [VirtualEnv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip)
- [Latest Application](https://github.com/jerehops/Electronic-Prescription)

## Windows
### Installing prerequistes
- Open your command prompt
- Change directory to Electronic-Prescription
- Run command 'python3 -m venv venv' (To create a virtual environment)
- Run command '.\venv\Script\activate.bat' (To enter virtual environment)
- Run command 'pip install -r requirement.txt' (To install all the dependencies)

### Setting up application
- Run command 'set FLASK_APP=wsgi.py'
- Run command 'set FLASK_ENV=development'
- Run command 'set E_PRESC_SENDGRID_API_KEY=<API-KEY>' (API key not included. Please request from project members)
- Run command 'flask run'
  
*Then run, http://127.0.0.1:5000 on browser*

## Unix
### Installing prerequistes
- Open your command prompt
- Change directory to Electronic-Prescription
- Run command 'python3 -m venv venv' (To create a virtual environment)
- Run command 'source venv/bin/activate' (To enter virtual environment)
- Run command 'pip install -r requirement.txt' (To install all the dependencies)
  
### Setting up application
- Run command 'export FLASK_APP=wsgi.py'
- Run command 'export FLASK_ENV=development'
- Run command 'export E_PRESC_SENDGRID_API_KEY=<API-KEY>' (API key not included. Please request from project members)
- Run command 'flask run'
  
*Then run, http://127.0.0.1:5000 on browser* 

