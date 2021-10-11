from flask import render_template, request, redirect, url_for, g
from app import webapp
from app import hash
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

# get password from 'user' table in our database
def user_get_password(email):
    table = dynamodb.Table('user')
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response['Item']['password']

@webapp.route('/login', methods = ['GET'])
# display a web page that allows users to enter their names and passwords to log into the system
def user_login():
    return render_template("login.html", title="Welcome to the Health Recording System")

@webapp.route('/login-check', methods = ['POST'])
# determine whether or not to log in the users by checking whether their entered passwords match their registered passwords
def user_login_main():
    
    email_enter = request.form.get('email', "")
    password_enter = request.form.get('password', "")
    password_enter_hashed = hash.hash_new_password(password_enter)

    row = [email_enter, password_enter]
    print("login information: ", row[0], row[1])

    # check user login with our database
    if email_enter == '' or password_enter == '':
        return "Error: All fields are required!"
    else:
        # check email
        if checkEmail(email_enter) == True:
            # email not registered
            return "Wrong email!"
        # email correct
        else:
            # fetch real password
            password = user_get_password(email_enter)
            # entered password and stored password match
            if password == password_enter_hashed:
                print("LOG-IN: ", email_enter)
                return redirect(url_for('main_pages', email=row[0]))
            # entered password and stored password don't match
            else:
                return "Wrong password!"