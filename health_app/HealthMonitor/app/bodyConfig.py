from flask import render_template, url_for, session, redirect, request
from app import webapp
from datetime import datetime, timedelta
from pytz import timezone
import time
import collections
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from flask import Markup
import random

ZONE = 'Canada/Eastern'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# get user name from 'user' table in our database
def get_username(email):
    table = dynamodb.Table('user')
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response['Item']['user_name']

# insert the provided user data (age, gender, weight, height, waist, hip, heart, blood, step, sleep, water, vegetable), calculated indicators (BMI, WHR, calories) and time into our database
def userdata_putItem(time, email, user_name, age, gender, weight, height, waist, hip, heart, blood, step, sleep, water, vegetable, bmi, whr, calorie):
    table = dynamodb.Table('userdata')
    response = table.put_item(
        Item={
            'time': time,
            'email': email,
            'user_name': user_name,
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'waist': waist,
            'hip': hip,
            'heart_rate': heart,
            'blood_pressure': blood,
            'step': step,
            'sleep': sleep,
            'water': water,
            'vegetable': vegetable,
            'BMI': bmi,
            'WHR': whr,
            'calorie': calorie
        },
        ConditionExpression="attribute_not_exists(email)",
    )
    return response

@webapp.route('/configure/<string:email>', methods = ['GET'])
# display a web page that allows users to enter their names and passwords to log into the system
def bdconfigure(email):
    return render_template("configure.html", email_display=email)

@webapp.route('/configure-data/<string:email>', methods = ['POST'])
def configure_data(email):

    # get user name
    username = get_username(email)
    print(username)

    time = datetime.now(timezone(ZONE))
    time = str(time)

    age = request.form.get('age', "")
    gender = request.form.get('gender', "")
    weight = request.form.get('weight', "")
    height = request.form.get('height', "")
    waist = request.form.get('waist', "")
    hip = request.form.get('hip', "")
    heart = request.form.get('heart', "")
    # optional choices
    blood = request.form.get('blood', "")
    step = request.form.get('steps', "")
    sleep = request.form.get('sleep', "")
    water = request.form.get('water', "")
    vegetable = request.form.get('vegetable', "")

    if age == '' and gender == '' and weight == '' and height == '' and waist == '' and hip == '' and heart == '':
        return "Error: You must fill all required fields !"

    # calculate BMI
    bmi = float(weight)/((float(height)/100)**2)   # height is in cm
    # calculate WHR
    whr = float(waist)/float(hip)
    # calculate calories
    if step != '':
        calorie = float(6.54e-4)*float(step)*float(weight)
    else:
        calorie = 0
    if blood == '':
        blood = 0
    if sleep == '':
        sleep = 0
    if water == '':
        water = 0
    if vegetable == '':
        vegetable = 0

    user_data = [age, gender, weight, height, waist, hip, heart, "optional input:", blood, step, sleep, water, vegetable]

    # insert the provided user data into our database
    userdata_putItem(time, email, username, Decimal(age), gender, Decimal(weight), Decimal(height), Decimal(waist),
                     Decimal(hip), Decimal(heart), Decimal(blood), Decimal(step), Decimal(sleep), Decimal(water),
                     Decimal(vegetable), round(Decimal(bmi), 1), round(Decimal(whr), 2), round(Decimal(calorie), 0))




    output = ''

    if bmi < 18.5:
        output = "BMI result: Underweight \n \u2022 Risk: increase the risk for osteoporosis, anemia, hair loss and fertility problems.\n \u2022 To eat more often to consume enough calories to gain weight(six small meals spread throughout the day instead of trying to pack more into three meals)\n \u2022 Consume nutrient-dense foods, such as lean protein, whole grains, legumes, low-fat dairy products, nuts and seeds and fruits and vegetables.\n \u2022 More strength training, approximately two to three days per week. \n\n\n"
    elif bmi<25.0:
        output = "BMI result: Normal \n \u2022 Keep current habits, try to avoid foods that are high in saturated fat, cholesterol, sugars and sodium, as these can increase your risks for certain health conditions. \n\n\n"
    elif bmi<29.9:
        output = "BMI result: Overweight \n \u2022 Risk: Increase the risk of many health problems, including diabetes, heart disease, and certain cancers.\n \u2022 To eating fewer and meals should be low carb, which limits carbs to 20–50 carbs per day. Each meal should have protein, healthy fats, veggies, and a small portion of complex carbohydrates, such as whole grains.\n \u2022 losing 1–2 pounds per week, try going to the gym three to four times a week to workout, including lifting weights, and some cardio workouts such as walking, jogging, running, cycling, or swimming.\n \u2022 Set weight goals and find someone could support you and encourage you. \n\n\n"
    else:
        output = "BMI result: Obesity \n \u2022 Risk:To causes a large number of health conditions, including heart disease, stroke, diabetes, high blood pressure, unhealthy cholesterol, asthma, sleep apnea, gallstones, kidney stones, infertility, and as many as 11 types of cancers, including leukemia, breast, and colon cancer. \n \u2022 Consume less fat, Eating more vegetables and fruits help keep calories reasonable and reduce the risk of overeating. \n \u2022 Regular weight training, find a professional trainer to design training plans, including strength training, and some cardio workouts such as walking, jogging, running, cycling, or swimming. \n \u2022 Try to reduce daily stress, stress may trigger a brain response that changes eating patterns and leads to cravings for high-calorie foods. \n \u2022 Set weight goals and find someone could support you and encourage you. \n \u2022 Weight-loss medications, a doctor will sometimes prescribe medication, such as orlistat (Xenical) to help a person lose weight. \n\n\n"
    
    if int(blood) != 0:
        if int(blood) >= 140 :
            output = output + "High Blood Pressure: \n \u2022 Reduce sodium in your diet, put less salt during cooking. \n \u2022 Quit smoking. \n \u2022 Limit the amount of alcohol you drink. \n \u2022 Monitor your blood pressure at home and see your doctor regularly.\n\n"

    if int(sleep) != 0:
        sleepless = "Lack of Sleeping: \n \u2022 Short-term effects on lacking of sleep: brain will fog, making it difficult to concentrate and make decisions.\n \u2022 Long-term effects on lacking of sleep: closely associated with hypertension, heart attacks and strokes, obesity, diabetes, depression and anxiety, decreased brain function, memory loss, weakened immune system, lower fertility rates and psychiatric disorders.\n \u2022 Daily sunlight or artificial bright light can improve sleep quality and duration\n \u2022 Don’t consume caffeine late in the day. \n \u2022 Reduce irregular or long daytime naps. \n \u2022 Try to sleep and wake at consistent times.\n \u2022 Relax and clear your mind in the evening.\n \u2022 Get a comfortable bed, mattress, and pillow.\n \u2022 Putting any smart mobile devices away.\n\n"
        oversleep = "Oversleeping: \n \u2022 Effects on oversleeping: increase the risk for diabetes; more likely to become obese; cause head pain; suffer from back pain; increase the risk of heart disease.\n \u2022 Change your alarm habits and resist hitting the snooze button.\n \u2022 Avoid sleeping in on weekends, even when you really want to.\n \u2022 Dodge the urge to take a nap  Improve your morning routine & day-to-day habits.\n \u2022 Avoid blue light before bed.\n \u2022 Create an ideal sleeping environment.\n\n"
        if int(age) <= 17 and int(sleep) < 8:
            output = output + sleepless
        elif int(age) <= 17 and int(sleep) > 12:
            output = output + oversleep
        elif int(age) <= 64 and int(sleep) < 7:
            output = output + sleepless
        elif int(age) <= 64 and int(sleep) >11:
            output = output + oversleep
        elif int(age) >=65 and int(sleep) <7:
            output = output + sleepless
        elif int(age) >=65 and int(sleep) >10:
            output = output + oversleep
        else:
            output = output + "Your sleeping is current in a good condition. \n\n"

    if int(water) != 0:
        if gender == 'Male' and int(water) > 9:
            output = output + '--Drinking too much water: \n \u2022 As you intake more water you can begin to flush water soluble vitamins and minerals.\n\n'
        elif gender == 'Male' and int(water) < 4:
            output = output + '--Should drink more water:\n \u2022 Don’t drinking enough water would lead to some health issues like high blood pressure and kidney stones.\n\n'
        elif gender == 'Female' and int(water) > 7:
            output = output + '--Drinking too much water: \n \u2022 As you intake more water you can begin to flush water soluble vitamins and minerals.\n\n'
        elif gender == 'Female' and int(water) < 3:
            output = output + '--Should drink more water:\n \u2022 Don’t drinking enough water would lead to some health issues like high blood pressure and kidney stones.\n\n'
        else:
            output = output + "--The amount of water you drink is at a good level. Please keep your habits \n\n"

    if int(vegetable) != 0:
        if int(vegetable) < 30:
            output = output + '--Should eat more vegetable: \n \u2022 half of your plate at any given meal—about 30 percent vegetables and 20 percent fruit. \n\n'
        else:
            output = output + '--Your dietary habit is good, and please remember to keep half of your plate at any given meal—about 30 percent vegetables and 20 percent fruit.\n\n'

    mealplan1 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Egg and avocado toast\n   \u2022 2 eggs\n   \u2022 1 slice of Ezekiel toast\n   \u2022 1/2 avocado\n Lunch — Salad with grilled chicken\n   \u2022 2 cups (40 grams) of spinach\n   \u2022 4 ounces (112 grams) of grilled chicken\n   \u2022 1/2 cup (120 grams) of chickpeas\n   \u2022 1/2 cup (25 grams) of shredded carrots\n   \u2022 1 ounce (28 grams) of goat cheese\n   \u2022 Balsamic vinaigrette\n Dinner — Cod with quinoa and broccoli\n   \u2022 5 ounces (140 grams) of baked cod\n   \u2022 1 tablespoon (15 ml) of olive oil\n   \u2022 3/4 cup (138 grams) of quinoa\n   \u2022 2 cups (176 grams) of roasted broccoli </p>'
    mealplan2 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Healthy yogurt bowl\n   \u2022 1 cup (245 grams) of full-fat plain yogurt\n   \u2022 1 cup (123 grams) of raspberries\n   \u2022 2 tablespoons (28 grams) of sliced almonds\n   \u2022 2 tablespoons (28 grams) of chia seeds\n   \u2022 1 tablespoon (14 grams) of unsweetened coconut\n Lunch — Mozzarella wrap\n   \u2022 2 ounces (46 grams) of fresh mozzarella\n   \u2022 1 cup (140 grams) of sweet red peppers\n   \u2022 2 slices of tomato\n   \u2022 1 tablespoon (15 grams) of pesto\n   \u2022 1 small, whole-grain wrap\n Dinner — Cod with quinoa and broccoli\n   \u2022 1 small sweet potato (60 grams)\n   \u2022 1 teaspoon (5 grams) of butter\n   \u2022 4 ounces (112 grams) of wild-caught salmon\n   \u2022 1 cup (88 grams) of roasted Brussels sprouts</p>'
    mealplan3 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Oatmeal\n   \u2022 1 cup (81 grams) of oatmeal cooked in 1 cup (240 ml) of unsweetened almond milk\n   \u2022 1 cup (62 grams) of sliced apple\n   \u2022 1/2 teaspoon of cinnamon\n   \u2022 2 tablespoons (32 grams) of natural peanut butter\n Lunch — Veggie and hummus wrap\n   \u2022 1 small whole-grain wrap\n   \u2022 2 tablespoons (32 grams) of hummus\n   \u2022 1/2 avocado\n   \u2022 2 slices of tomato\n   \u2022 1 cup (20 grams) of fresh arugula\n   \u2022 1 ounce (28 grams) of muenster cheese\n Dinner — Chili\n   \u2022 3 ounces (84 grams) of ground turkey\n   \u2022 1/2 cup (120 grams) of black beans\n   \u2022 1/2 cup (120 grams) of kidney beans\n   \u2022 1 cup (224 grams) of crushed tomatoes</p>'
    mealplan4 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Peanut butter and banana toast with eggs\n   \u2022 2 fried eggs\n   \u2022 1 slice of Ezekiel toast\n   \u2022 2 tablespoons (32 grams) of natural peanut butter\n   \u2022 1/2 sliced banana\n Lunch — On-the-go sushi\n   \u2022 1 cucumber and avocado sushi roll made with brown rice\n   \u2022 1 vegetable roll with brown rice\n   \u2022 2 pieces of salmon sashimi and a green salad\n Dinner — Black bean burger\n   \u2022 1 cup (240 grams) of black beans\n   \u2022 1 egg\n   \u2022 Chopped onion\n   \u2022 Chopped garlic \n   \u2022 1 tablespoon (14 grams) of breadcrumbs\n   \u2022 2 cups (20 grams) of mixed greens\n   \u2022 1 ounce (28 grams) of feta cheese</p>'
    mealplan5 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Breakfast smoothie\n   \u2022 1 scoop of pea protein powder\n   \u2022 1 cup (151 grams) of frozen blackberries\n   \u2022 1 cup (240 ml) of coconut milk\n   \u2022 1 tablespoon (16 grams) of cashew butter\n   \u2022 1 tablespoon (14 grams) of hemp seeds\n Lunch — Kale salad with grilled chicken\n   \u2022 2 cups (40 grams) of kale\n   \u2022 4 ounces (112 grams) of grilled chicken\n   \u2022 1/2 cup (120 grams) of lentils\n   \u2022 1/2 cup (25 grams) of shredded carrots\n   \u2022 1 cup (139 grams) of cherry tomatoes\n   \u2022 1 ounce (28 grams) of goat cheese\n   \u2022 Balsamic vinaigrette\n Dinner — Shrimp fajitas\n   \u2022 4 ounces (112 grams) of grilled shrimp\n   \u2022 2 cups (278 grams) of onions and peppers sauteed in 1 tablespoon (15 ml) of olive oil\n   \u2022 2 small corn tortillas\n   \u2022 1 tablespoon of full-fat sour cream \n   \u2022 1 ounce (28 grams) of shredded cheese </p>'
    mealplan6 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Oatmeal\n   \u2022 1 cup (81 grams) of oatmeal cooked in 1 cup (240 ml) unsweetened almond milk\n   \u2022 1 cup (123 grams) of blueberries\n   \u2022 1/2 teaspoon of cinnamon\n   \u2022 2 tablespoons (32 grams) of natural almond butter\n Lunch — Tuna salad\n   \u2022 5 ounces (140 grams) of canned tuna\n   \u2022 1 tablespoon (16 grams) of mayo\n   \u2022 Chopped celery\n   \u2022 2 cups (40 grams) of mixed greens\n   \u2022 1/4 sliced avocado\n   \u2022 1/2 cup (31 grams) of sliced green apple\n Dinner — Chicken with veggies\n   \u2022 5 ounces (120 grams) of baked chicken\n   \u2022 1 cup (205 grams) of roasted butternut squash cooked in 1 tablespoon (15 ml) of olive oil\n   \u2022 2 cups (176 grams) roasted broccoli</p>'
    mealplan7 = '<h6> Meal Plan for you:</h6> <p>Breakfast — Omelet\n   \u2022 2 eggs\n   \u2022 1 ounce (28 grams) of cheddar cheese\n   \u2022 1 cup (20 grams) of spinach cooked in 1 tablespoon (15 ml) of coconut oil\n   \u2022 1 cup (205 grams) of sautéed sweet potatoes\n Lunch — On-the-go Chipotle\n   \u2022 1 Chipotle burrito bowl made with romaine lettuce, Barbacoa chicken, brown rice, 1/2 serving of guacamole and fresh salsa\n Dinner — Pasta with pesto and beans\n   \u2022 1 cup (140 grams) of brown-rice pasta or whole-wheat pasta\n   \u2022 1 tablespoon (14 grams) of pesto\n   \u2022 1/4 cup (60 grams) of cannellini beans\n   \u2022 1 cup (20 grams) of spinach\n   \u2022 1 cup (139 grams) of cherry tomatoes\n   \u2022 1 tablespoon (5 grams) of grated parmesan cheese</p>'

    mealPlan = [mealplan1, mealplan2, mealplan3, mealplan4, mealplan5, mealplan6, mealplan7]
    rand_x = random.randint(0, 6)
    output = output + mealPlan[rand_x]
    output = Markup(output.replace('\n', '<br>'))

    return render_template('message.html', email=email, message = output)