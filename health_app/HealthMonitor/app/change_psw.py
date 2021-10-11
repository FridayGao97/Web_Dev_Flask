from flask import render_template, request, g
from app import webapp
from app import hash
import sys
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

# update password to database
def update_password(email, password):
    table = dynamodb.Table('user')
    response = table.update_item(
        ExpressionAttributeNames={
            '#P': 'password'
        },
        ExpressionAttributeValues={
            ':p': password
        },
        Key={
            'email': email
        },
        UpdateExpression='SET #P = :p',
        ReturnValues="ALL_NEW"
    )

@webapp.route('/new_psw', methods = ['GET'])
# display a web page that allows users to change their passwords after their old passwords are confirmed
def change_psw():
    return render_template("new_psw.html", title="Change Password")

@webapp.route('/new_psw_check', methods = ['POST'])
# save the new password into the database after the old password is confirmed
def change_psw_save():
    # get input
    email = request.form.get('email', "")
    old_psw = request.form.get('oldpassword', "")
    new_psw_1 = request.form.get('new1password', "")
    new_psw_2 = request.form.get('new2password', "")

    # check with our database
    if email == '' or old_psw == '' or new_psw_1 == '' or new_psw_2 == '':
        return "Error: All fields are required!"
    else:
        # check email
        if checkEmail(email) == True:
            # email not registered
            return "Wrong email!"
        # email correct
        else:
            # fetch real password (the stored old password)
            password = user_get_password(email)
            # hash the entered old password
            old_psw_hashed = hash.hash_new_password(old_psw)
            # entered old password matches with stored old password
            if old_psw_hashed == password:
                # newly entered passwords match
                if new_psw_1 == new_psw_2:
                    # hash the newly entered password
                    new_psw_hashed = hash.hash_new_password(new_psw_1)
                    # update the database
                    update_password(email, new_psw_hashed)
                    return render_template("login.html")
                else:
                    return "New passwords don't match!"
            else:
                return "Wrong old password!"