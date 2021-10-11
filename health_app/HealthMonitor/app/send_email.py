from flask_mail import Mail, Message
import random
import string
from flask import render_template, redirect, url_for, request, g
from app import webapp
from app import hash
import sys
import os
from werkzeug.utils import secure_filename
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

webapp.config['MAIL_SERVER']='smtp.gmail.com'
webapp.config['MAIL_PORT'] = 465
webapp.config['MAIL_USERNAME'] = 'ece1779healthapp@gmail.com'
webapp.config['MAIL_PASSWORD'] = 'ece1779pass'
webapp.config['MAIL_USE_TLS'] = False
webapp.config['MAIL_USE_SSL'] = True

# initialize mail object
mail = Mail(webapp)

def get_random_pswd(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    randmstr = ''.join(random.choice(letters) for i in range(length))
    print("Random string is:", randmstr)
    return randmstr

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

@webapp.route('/recovery')
def recoverByEmail():
    return render_template('recovery.html')

# send email with password generated randomly
@webapp.route("/email", methods=["POST"])
def send_email():
    # recipient's email
    toEmail = request.form.get('email', "")
    if toEmail == "":
        return "Error: All fields are required!"
    # check email
    if checkEmail(toEmail) == True:
        return "Error: This email has not been registered before, please register at first!"
    else:
        temp_pswd = get_random_pswd(8)
        # hash this password
        temp_pswd_hashed = hash.hash_new_password(temp_pswd)
        msg = Message(subject="Health Recording System: recover password", sender='ece1779healthapp@gmail.com',
                      recipients=[toEmail])
        msg.body = "We have reset the password for you, and The Reset Password is : " + temp_pswd
        update_password(toEmail, temp_pswd_hashed)
        mail.send(msg)
        print("Send!!!")
        temp_mesg = 'The password has been sent to the email (%s), Please check the Inbox or Spam' % (toEmail)
        return render_template('recovery.html', message=temp_mesg)



def send_manager(output):
    # recipient's email
    toEmail1 = "qixuan.zhang@mail.utoronto.ca"
    toEmail2 = "shixiong.gao@mail.utoronto.ca"

    msg1 = Message(subject="Health Recording System: Manager Report", sender='ece1779healthapp@gmail.com',
                    recipients=[toEmail1])
    msg1.body = "Good Morning, Qixuan \n" + output

    with webapp.app_context():
        mail.send(msg1)

    print("SendToQixuan")

    msg2 = Message(subject="Health Recording System: Manager Report", sender='ece1779healthapp@gmail.com',
                    recipients=[toEmail2])
    msg2.body = "Good Morning, Shixiong \n" + output

    with webapp.app_context():
        mail.send(msg2)


    print("SendToShixiong!!!")

    return True

