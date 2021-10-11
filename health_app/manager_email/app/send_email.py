from flask_mail import Mail, Message
import random
import string
from flask import render_template, redirect, url_for, request, g
from app import webapp

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

