# pythonAnywhere

# 1> wsgi 
# https://www.pythonanywhere.com/user/ananya1989/files/var/www/ananya1989_pythonanywhere_com_wsgi.py?edit
# # This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = '/home/ananya1989/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
#from flask_app import app as application  # noqa
from app import app as application  # noqa

# 2> bash
# https://www.pythonanywhere.com/user/ananya1989/consoles/29531687/ 
pip install pymysql

# 3> เขียนคำสั่ง sql
# https://www.pythonanywhere.com/user/ananya1989/consoles/29531300/
SHOW DATABASES;
use ananya1989$default;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user (username, email, password)
VALUES ('charlotte_aus', 'charlotte_aus@example.com', 'securepassword123');
