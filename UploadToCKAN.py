################################################################################

# Smallest possible example of uploading a code to CKAN by its RESTful server
# that includes connection with Oracle and validation after the upload

################################################################################

# SPECIAL LIBRARY REQUIRED
# execute: 'pip install requests'
import requests

# SPECIAL LIBRARY REQUIRED
# execute: 'pip install cx_oracle'
import cx_Oracle

# Used to generate a dinamic nome to the file
import datetime

# Used for read a string JSON as an array
import json

# Timer
import time

# Used to avoid using the webcache
import random

################################################################################

# Queries how many resources a dataset already has
# Later it will be used to validate whether the job was successfully done
def get_num_resouces(dataset):
    response = requests.get('http://myckansiteexample.com/api/3/action/package_show?id=' + dataset + '&m=' + str(random.random()))
    response = response.json()
    return response['result']['num_resources']

################################################################################

qty_before_upload = get_num_resouces('courses') # courses: the dataset name

# Oracle connection string
uid = 'username'
pwd = 'p4ssw0rd'
db = '(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = 123.56.231.78)(PORT = 1529))(CONNECT_DATA = (SERVER = DEDICATED)(SID = MYSID)))'

connection = cx_Oracle.connect(uid + '/' + pwd + '@' + db)
cursor = connection.cursor()

cursor.execute('''
    SELECT
        *
    FROM
        COURSES
    WHERE
        1 = 1
''')

result = cursor.fetchone()

content = ''

if result == None:
    print('Empty table. No rows to create a file to CKAN.')
    exit
else:
    while result:
        for column in result:
            content  = content + '"' + str(column).replace('"', '') + '", '
        content = content + '""\n'
        result = cursor.fetchone()

cursor.close()
connection.close()

year, month, date = str(datetime.datetime.now()).split('-')
filename = 'Courses ' + month + '-' + year

# Saves the CSV file
file = open(filename + '.csv', 'w')
file.write(content)
file.close()

# Upload the CSV file to 'Courses'
requests.post(
    'http://myckansiteexample.com/api/action/resource_create',
    data={
        # Required
        'package_id':'Courses',
        'name'      : filename, # Resource title (it appears in bold on the page)

        # Opticional (default key-value)
        'author'          : 'John Doe',
        'author_email'    : 'john_doe@myckansiteexample.com',
        'url'             : 'Courses Catalog', # URL actually means source of data
        'maintainer'      : 'Charles Darwin',
        'maintainer_email': 'charles_darwin@myckansiteexample.com',
        'version'         : '1.0',

        # Keys with any name or value
        'Language': 'English',
        'Partner' : 'Google'
        # etc...
    },
    headers={'X-CKAN-API-Key': '548a5cd3-d364-43af-ae96-1da22bcb46a4'},
    files=[('upload', open(filename + '.csv'))]
)

# Personal secret key: 548a5cd3-d364-43af-ae96-1da22bcb46a4

# Waits 5 seconds so CKAN has time to processes it
time.sleep(5)

# New qty of resources
qty_after_upload = get_num_resouces('Courses')

# Validates whether there's a new resource or not
if(qty_after_upload != qty_before_upload + 1):
    print('An error in the process kept the file from being inserted in CKAN.')
else:
    print('Resource uplodad with success.')

################################################################################