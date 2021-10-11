from flask import render_template, request, redirect, jsonify, url_for, g
from app import webapp
from app import hash
import re
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# query email from 'user' table in our database
def user_query_email(email):
    table = dynamodb.Table('user')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    records = []
    for i in response['Items']:
        records.append(i)
    return records

# query username from 'user' table in our database
def user_query_username(username):
    table = dynamodb.Table('user')
    response = table.query(
        IndexName='UserNameIndex',
        KeyConditionExpression=Key('user_name').eq(username)
    )
    records = []
    for i in response['Items']:
        records.append(i)
    return records

# check the email provided is registered before or not
def checkEmail(email):
    # run the query
    temp = user_query_email(email)
    # if not registered
    if len(temp) == 0:
        return True
    # if registered before
    else:
        return False

# check the username provided is registered before or not
def checkUsername(username):
    # run the query
    temp = user_query_username(username)
    # if not registered
    if len(temp) == 0:
        return True
    # if registered before
    else:
        return False

# insert the provided user information (username, email, password) into our database
def user_putItem(email, user_name, password):
    table = dynamodb.Table('user')
    response = table.put_item(
        Item={
            'email': email,
            'user_name': user_name,
            'password': password,
        }
    )
    return

@webapp.route('/register')
# display a web page that allows users to register their names, emails and passwords
def user_register():
    return render_template("register.html", title="Register")

@webapp.route('/register-verify', methods=['POST'])
# save the registered user information (username, email, password) into our database
def user_register_save():

    name = request.form.get('username', "")
    email = request.form.get('email', "")
    password = request.form.get('password', "")
    hashed_password = hash.hash_new_password(password)

    if name == '' or email == '' or password == '':
        return "Error: All fields are required!"

    # check username
    if not checkUsername(name):
        return "success: False, this username has already been used!"

    # check email
    if not checkEmail(email):
        # already registered email
        return "success: False, this email has already been registered!"
    # new registered email address
    else:
        user_putItem(email, name, hashed_password)

        '''
        # check the email address format
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # valid format
        if (re.search(regex,email)):
            # insert the provided user information into our database
            user_putItem(email, name, hashed_password)
        else:
            return "success: False, please enter the email as email format!"
        '''

    message = "Name: " + name + " Email: " + email + " Password: " + password
    return render_template("register.html", message=message)