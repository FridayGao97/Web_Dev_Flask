from flask import render_template, url_for, session, redirect, request
from app import webapp
from datetime import datetime, timedelta
import collections
from pytz import timezone,utc
import boto3
from boto3.dynamodb.conditions import Key

from app import send_email

ZONE = 'Canada/Eastern'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

global manger
manger = True

# get user name from 'user' table in our database
def get_username(email):
    table = dynamodb.Table('user')
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response['Item']['user_name']

# scan the 'userdata' table from our database
def scan_userdata(email):
    table = dynamodb.Table('userdata')
    response = table.scan(
        ExpressionAttributeValues={
            ':e': email
        },
        FilterExpression='email = :e',

        #TODO:
        #to try if it work?
        #KeyConditionExpression: 'Time = :time',
        #ScanIndexForward: True,
        # true = ascending, false = descending
        #end todo

    )
    return response




#TODO: CHECK THIS FUNCTION
# scan the 'user' table from our database
def getColumnItems():
    table = dynamodb.Table('user')
    resp = table.scan(AttributesToGet=['email'])

    return resp['Items']

#background thread
def backgroundProcess():
    print("start bg")
    global manger
    manger = True
    while True:

        nowtime = datetime.now(timezone(ZONE))
        weekday = nowtime.strftime('%A')
        hour = nowtime.strftime('%H:%M:%S')
        #send email to manager evey Monday 7am
        if manger:
            #if weekday == 'Monday':
            if weekday == 'Monday':
                #if hour == '07:00:00':
                if hour == '19:14:00':
                    manger = False
                    res = manager_email()
                    print("true", res)
        else:
            #if hour != '07:00:01' and manger == False:
            if hour != '19:14:00' and manger == False:
                manger = True

#send email to manager inbox
def manager_email():

    #The cursor should looks like: (order isn't matter)
    # cursor = [{'email':'sds@sdsd.com','user_name':'lll','password':'1231213'},{'time':'2020-09-19','user_name':'hhh','password':'1231213'}]
    cursor = getColumnItems()
    
    userlen = len(cursor)
    #message body for email
    output = ''

    userstr = ''

    Children = 0
    Adolescence = 0
    Adults = 0
    Seniors = 0
    underweight = 0
    normalweight = 0
    overweight = 0
    obesity = 0
    female = 0
    male = 0
    other_gender = 0
    riskWHRlow = 0
    riskWHRmed = 0
    riskWHRHih = 0
    avgstep = 0
    avgcalorie = 0

    #iterate to get all user
    for user in cursor:
        # scan user data
        username = user['email']
        
        weight = 0
        BMI = 0
        WHR = 0
        Daily_Steps = 0
        Calorie = 0
        age = 0
        gender = ''
        
        #iterate to get all data for certain user
        userdata = scan_userdata(user['email'])
        num_samples = len(userdata['Items'])
        for item in userdata['Items']:
            age = int(item['age'])
            gender = str(item['gender'])
            weight = weight + float(item['weight'])
            BMI = BMI + float(item['BMI'])
            WHR = WHR + float(item['WHR'])
            Daily_Steps = Daily_Steps + int(item['step'])
            Calorie = Calorie + float(item['calorie'])
        
        #detail data analysis for each user
        userstr = userstr + '  \u2022  '+str(username) + ': ' + str(age)+ 'years old; ' + gender + '.  --Average Weight: ' + str(float(weight/num_samples)) + ';  Average BMI: ' + str(float(BMI/num_samples)) + ';  Average WHR: ' + str(float(WHR/num_samples)) + ';  Average Daily steps: ' + str(float(Daily_Steps/num_samples)) + ';  Average Daily Calories: ' + str(float(Calorie/num_samples)) + '\n'
        
        #category each user 
        #for BMI
        avg = float(BMI/num_samples)
        if avg < 18.5:
            underweight = underweight + 1
        elif avg < 25.0:
            normalweight = normalweight + 1
        elif avg < 29.9:
            overweight = overweight + 1
        else:
            obesity = obesity + 1

        #for age and WHR
        avg = float(WHR/num_samples)
        if gender == 'Female':
            female += 1
            if avg < 0.8:
                riskWHRlow += 1
            elif avg< 0.86:
                riskWHRmed += 1
            else:
                riskWHRHih += 1
        elif gender == 'Male':
            male += 1
            if avg < 0.95:
                riskWHRlow += 1
            elif avg< 1.0:
                riskWHRmed += 1
            else:
                riskWHRHih += 1
        else:
            other_gender += 1

        #for age
        if age < 13:
            Children += 1
        elif age < 19:
            Adolescence += 1
        elif age < 60:
            Adults += 1
        else:
            Seniors += 1

        avgstep = avgstep + float(Daily_Steps/num_samples)
        avgcalorie = avgcalorie + float(Calorie/num_samples)
        
    #email body
    output = 'The total number of users in our health monitor app: ' + str(userlen) + '\n'
    output = output + 'Summary For All Users: \n' + ' \u2022  # of Children(0~12): ' + str(Children) + ' (%.2f)'%(Children/(Children+Adolescence+Adults+Seniors)*100) + ';   Adolescence(13~18): ' + str(Adolescence) + ' (%.2f)'%(Adolescence/(Children+Adolescence+Adults+Seniors)*100) +';   Adult(19~59): ' + str(Adults) + ' (%.2f)'%(Adults/(Children+Adolescence+Adults+Seniors)*100) +';   Seniors(60+): ' + str(Seniors) + ' (%.2f)'%(Seniors/(Children+Adolescence+Adults+Seniors)*100) +'\n'
    output = output + ' \u2022  # of Female: ' + str(female) + ' (%.2f)'%(female/(female+male+other_gender)*100) + ';   # of Male: ' + str(male) + ' (%.2f)'%(male/(female+male+other_gender)*100) +';   # of Others: ' + str(other_gender) + ' (%.2f)'%(other_gender/(female+male+other_gender)*100) + '\n'
    output = output + ' \u2022  Average Daily steps across all users: ' + str(float(avgstep/userlen)) + '\n'
    output = output + ' \u2022  Average Daily Calorie consumed by all users: ' + str(float(avgcalorie/userlen)) + '\n'
    output = output + ' \u2022  # of Underweight' + str(underweight) + ' (%.2f)'%(underweight/(underweight+normalweight+overweight+obesity)*100) + ';   # of Normal weight: ' + str(normalweight) + ' (%.2f)'%(normalweight/(underweight+normalweight+overweight+obesity)*100) + ';   # of Overweight: ' + str(overweight) + ' (%.2f)'%(overweight/(underweight+normalweight+overweight+obesity)*100) + ';   # of Obesity: ' + str(obesity) + ' (%.2f)'%(obesity/(underweight+normalweight+overweight+obesity)*100) + '\n' 
    output = output + ' \u2022  Health Risk based on WHR: \n' + '    -- Low(0.80 or lower for women/0.95 or lower for men: ' + str(riskWHRlow) + ' (%.2f)'%(riskWHRlow/(riskWHRlow+riskWHRmed+riskWHRHih)*100) + '\n' + '    -- Moderate(0.81–0.85 for women/0.96–1.0 for men: ' + str(riskWHRmed) + ' (%.2f)'%(riskWHRmed/(riskWHRlow+riskWHRmed+riskWHRHih)*100) + '\n' + '    -- High(0.86 or higher for women/1.0 or higher for men: ' + str(riskWHRHih) + ' (%.2f)'%(riskWHRHih/(riskWHRlow+riskWHRmed+riskWHRHih)*100) + '\n'
    
    output = output + '\n\n'
    if userlen <= 10:
        output = output + 'User Details for each one: \n'
        output = output + userstr
        output = output + '\n'
    
    sent = send_email.send_manager(output)
    if sent == True:
        print("Background thread running")
        return "Background thread running"
    else:
        print("Fail to run Background thread")
        return "Fail to run Background thread"

            



@webapp.route('/user-page/<string:email>', methods=['GET'])
def main_pages(email):
    
    # get user name
    username = get_username(email)

    # scan user data
    cursor = scan_userdata(email)

    '''
    cursor = []
    cursor.append(userdata)
    '''

    print('debug', cursor)

    user_data = {}
    user_data['Time'] = []
    user_data['User_name'] = []
    user_data['BMI'] = []
    user_data['WHR'] = []
    user_data['Heart_Rate'] = []
    user_data['Blood_Pressure'] = []
    user_data['Daily_Steps'] = []
    user_data['Calorie'] = []

    '''
    for item in cursor['Items']:
        print('a', item)
        user_data['Time'].append(item['time'])
        user_data['User_name'].append(item['user_name'])
        user_data['BMI'].append(item['BMI'])
        user_data['WHR'].append(item['WHR'])
        user_data['Heart_Rate'].append(item['heart_rate'])
        user_data['Blood_Pressure'].append(item['blood_pressure'])
        user_data['Daily_Steps'].append(item['step'])
        user_data['Calorie'].append(item['calorie'])
    '''
    count = 0
    #first chart x:time, y:weight
    weightdata = []
    BMIdata = []
    WHRdate = []

    for item in cursor['Items']:
        if count > 10:
            break
        print('a', item)
        count = count +1
        user_data['Time'].append(item['time'])
        user_data['User_name'].append(item['user_name'])
        user_data['BMI'].append(item['BMI'])
        user_data['WHR'].append(item['WHR'])
        user_data['Heart_Rate'].append(item['heart_rate'])
        user_data['Blood_Pressure'].append(item['blood_pressure'])
        user_data['Daily_Steps'].append(item['step'])
        user_data['Calorie'].append(item['calorie'])
        weightdata.append([item['time'],float(item['weight'])])
        BMIdata.append([item['time'],float(item['BMI'])])
        WHRdate.append([item['time'],float(item['WHR'])])



    user_data = zip(user_data['Time'], user_data['User_name'], user_data['BMI'], user_data['WHR'], user_data['Heart_Rate'], user_data['Blood_Pressure'], user_data['Daily_Steps'], user_data['Calorie'])

    #first chart x:time, y:weight
    weight_temp = sorted(weightdata, key=lambda x: x[0])

    weightlabels = []
    weightvalues = []

    # get all weight, BMI WHR etc., during that time
    for workeritem in weight_temp:
        #only higher than python3.3
        weightlabels.append(workeritem[0][5:16])
        weightvalues.append(int(workeritem[1]))

    maxweight = ((max(weightvalues)*1.2)//10+1)*10

    #BMI chart, x:time, y:BMI
    BMI_temp = sorted(BMIdata, key=lambda x: x[0])

    BMIlabels = []
    BMIvalues = []

    # get all weight, BMI WHR etc., during that time
    for workeritem in BMI_temp:
        #only higher than python3.3
        BMIlabels.append(workeritem[0][5:16])
        BMIvalues.append(workeritem[1])
    
    
    #WHR chart, x:time, y:WHR
    WHR_temp = sorted(WHRdate, key=lambda x: x[0])
    WHRlabels = []
    WHRvalues = []

    # get all weight, BMI WHR etc., during that time
    for workeritem in WHR_temp:
        #only higher than python3.3
        WHRlabels.append(workeritem[0][5:16])
        WHRvalues.append(workeritem[1])
    

    return render_template('mainpage.html', email=email, username=username, user_data=user_data, weightlabels=weightlabels, weightvalues=weightvalues, BMIlabels=BMIlabels, BMIvalues=BMIvalues, WHRlabels=WHRlabels, WHRvalues=WHRvalues, maxweight=maxweight)