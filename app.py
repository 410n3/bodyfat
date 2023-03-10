#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 22:14:02 2023

@author: maneeshradhakrishnan
"""

import streamlit as st
import pickle
import math
from streamlit_option_menu import option_menu
from sklearn.linear_model import LinearRegression
import gspread
import gspread_pandas as gspd
from google.oauth2 import service_account
from pandas import DataFrame
from gsheetsdb import connect
import pandas as pd
import random
import string
import re
from fpdf import FPDF
import os





den=pickle.load(open("den_pred.sav",'rb'))
bfper=pickle.load(open("bf_pred.sav",'rb'))

def bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip):
    # Calculating body fat percentage for males
    height=float(Height)
    height=height*2.54
    weight=float(Weight)
    weight=weight/2.205
    body_fat_perc=0
    bmr=0
    if gender == "Male":
        body_fat_perc= 495 / (1.0324 - 0.19077 * (math.log10(Abdomen - Neck)) + 0.15456 * (math.log10(height))) - 450
        bmr = (13.397*weight)+ (4.799*height) - (5.677*Age) + 88.362
# Calculating body fat percentage for females
    elif gender == "Female":
        body_fat_perc = 495 / (1.29579 - 0.35004 * (math.log10(Abdomen + Hip - Neck)) + 0.22100 * (math.log10(height))) - 450
        bmr=(9.247*weight) + (3.098*height) - (4.330*Age) + 447.593
    else:
        return "Invalid input. Please enter M or F for gender."
    user_update=[[body_fat_perc,Age,Weight,Height,Neck,Chest,Abdomen,Hip]]
    prediction=den.predict(user_update)
    user_update2=[[prediction[0],Age,Weight,Height,Neck,Chest,Abdomen,Hip]]
    prediction2=bfper.predict(user_update2)
    weight=float(Weight)
    height=float(Height)
    height=height*2.54 #cms
    weight=weight/2.205 #kgs
    bmi=weight/(height/100)**2
    bf=1.20*bmi+0.23*Age-16.2
    if bmi <= 18.5:  
        if bf > prediction2[0]:  
            conclusion = bf - prediction2[0]
            conclusion = round(conclusion, 0)
            bf1=round(prediction2[0] + conclusion,3)
            return bf1,bmi,bf,bmr
        else:
            conclusion = prediction2[0] - bf
            conclusion = round(conclusion, 0)
            bf1=round(prediction2[0] + conclusion,3)
            return bf1,bmi,bf,bmr
    elif bmi <= 24.9:
        if bf > prediction2[0]:  
            conclusion = bf - prediction2[0]
            conclusion = round(conclusion, 0)
            if conclusion>=7:
                conclusion=conclusion-6
                bf1=round(prediction2[0]-conclusion,3)
            else:
                conclusion=conclusion-2.5
                bf1=round(prediction2[0] + conclusion,3)
            return bf1,bmi,bf,bmr
        else:
            conclusion = prediction2[0]-bf
            conclusion = round(conclusion, 0)
            if conclusion>=7:
                conclusion=conclusion-6
                bf1=round(prediction2[0]-conclusion,3)
            else:
                conclusion=conclusion-2.5
                bf1=round(prediction2[0] + conclusion,3)
            return bf1,bmi,bf,bmr
        
            
    elif bmi <= 29.9:  
            if bf > prediction2[0]:  
                conclusion = bf - prediction2[0]
                conclusion = round(conclusion, 0)
                if conclusion>=10:
                    conclusion=conclusion-5
                    bf1=round(prediction2[0]-conclusion,3)
                else:
                    bf1=round(prediction2[0] + conclusion,3)
                return bf1,bmi,bf,bmr
            else:
                conclusion = prediction2[0]-bf
                conclusion = round(conclusion, 0)
                if conclusion>=10:
                    conclusion=conclusion-5
                    bf1=round(prediction2[0]-conclusion,3)
                else:
                    bf1=round(prediction2[0] + conclusion,3)
                return bf1,bmi,bf,bmr
    else:  
                if bf > prediction2[0]:  
                    conclusion = bf - prediction2[0]
                    conclusion = round(conclusion, 0)
                    if conclusion>=10:
                        conclusion=conclusion-5
                        bf1=round(prediction2[0]-conclusion,3)
                    else:
                        bf1=round(prediction2[0] + conclusion,3)
                    return bf1,bmi,bf,bmr
                    
                else:
                    conclusion = prediction2[0] - bf
                    conclusion = round(conclusion, 0)
                    if conclusion>=10:
                        conclusion=conclusion-5
                        bf1=round(prediction2[0]-conclusion,3)
                    else:
                        bf1=round(prediction2[0] + conclusion,3)
                    return bf1,bmi,bf,bmr
                    
def main():
    page_title="AI Bodyfat percentage calculator"
    page_icon=":chart_with_downwards_trend:" 
    st.set_page_config(page_title=page_title,page_icon=page_icon)
    st.markdown(""" <style> #MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
    st.title(page_icon + " " + page_title)
    
    selected=option_menu( 
        menu_title=None,
        options=["Predicting Bodyfat percent","Your target Calories intake","21 days weight loss guide"],
        orientation="horizontal"
        )

    ###
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    gc = gspread.authorize(credentials)
    sheet_url = st.secrets["private_gsheets_url"]
    sheet = gc.open_by_url(sheet_url).sheet1
    sheet_url_ui = st.secrets["private_gsheets_url1"]
    sheet_ui = gc.open_by_url(sheet_url_ui).sheet1
    

    # Insert a row into the Google Sheet.
    def insert_row(uid,gender ,name, email, Age, Weight, Height, bmi1, bmr1, bf2, bf1):
        row = [uid,gender,name, email, Age, Weight, Height, bmi1, bmr1, bf2, bf1]
        sheet.insert_row(row, 2)  # Insert the row at the second row (after the header).
        st.success('Stored for futher calculations.')
        ###
    def insert_row_ui(uid,name,email,age,weight,height,neck,chest,abdomen,hip):
        row = [uid,name, email, Age, Weight, Height, Neck, Chest, Abdomen, Hip]
        sheet_ui.insert_row(row, 2)  # Insert the row at the second row (after the header).
        st.success('Stored for futher calculations.')
        ###
    
    def validate_email(email):
        # A simple regex to validate email format
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    
    class PDF(FPDF):
            def body_composition(self,uid,name,age, weight, height, body_fat,bmr,neck,Chest,Abdomen,Hip,text):
                self.image('logo.png', x=10, y=10, w=44)
               
                self.ln(10) # add some space before the next row
                self.set_font('Helvetica', 'B', 20)
                self.set_text_color(0, 0, 0) # set font color to dark red
                self.set_fill_color(96, 252, 96)  # set background color to light blue
                self.cell(0, 15, 'Body Composition', 0, 1, 'C', True) # add background color
                
                self.set_font('Helvetica', '', 14)
                self.set_text_color(0, 0, 0) # set font color to black
                self.cell(50, 10, 'Uid:', 0, 0)
                self.cell(50, 10, str(uid), 0, 1)
                self.cell(50, 10, 'Name:', 0, 0)
                self.cell(50, 10, str(name), 0, 1)
                self.cell(50, 10, 'Age:', 0, 0)
                self.cell(50, 10, str(age) + ' yrs', 0, 1)
                self.cell(50, 10, 'Weight:', 0, 0)
                self.cell(50, 10, str(round(weight)) + ' kgs', 0, 1)
                self.cell(50, 10, 'Height:', 0, 0)
                self.cell(50, 10, str(height) + ' inches', 0, 1)
                
                self.ln(10) # add some space before the next row
                
                self.set_fill_color(112, 255, 107) # set background color to light yellow
                self.cell(0, 10, '', 0, 1, 'C', True) # add a separator line
                
                self.ln(10) # add some space before the next row
                
                self.set_font('Helvetica', '', 14)
                self.set_text_color(0, 0, 0) # set font color to black
                self.cell(50, 10, 'Neck measurement:', 0, 0)
                self.cell(50, 10, str(neck) + ' cms', 0, 1)
                self.cell(50, 10, 'Chest measurement:', 0, 0)
                self.cell(50, 10, str(Chest) + ' cms', 0, 1)
                self.cell(50, 10, 'Abdomen measurement:'+"  ", 0, 0)
                self.cell(50, 10, str(Abdomen) + ' cms', 0, 1)
                self.cell(50, 10, 'Hip measurement:', 0, 0)
                self.cell(50, 10, str(Hip) + ' cms', 0, 1)
                self.cell(50, 10, 'Body Fat Percentage:', 0, 0)
                self.cell(50, 10, str(body_fat) + '%', 0, 1)
                
                self.ln(10) # add some space before the next row
                
                self.set_fill_color(112, 255, 107) 
                self.cell(0, 10, '', 0, 1, 'C', True) # add a separator line
                
                self.ln(10) # add some space before the next row
                
                self.set_font('Helvetica', '', 14)
                self.set_text_color(0, 0, 0)
                pdf.write(5, text)

    
    
    
    
    
    
    def generate_id(length=8):
            alphanumeric = string.ascii_uppercase + string.digits
            id = ''.join(random.choice(alphanumeric) for _ in range(length))
            return id
    def classify_body_fat_percentage(gender, body_fat_percentage,bmr):
        if gender == "Female":
            if body_fat_percentage < 14:
                bmrf=bmr+400
                return f'Focus on weight gain  and  eat upto {bmrf} '
            elif 14 <= body_fat_percentage < 21:
                bmrf=bmr+400
                return f'Focus on weight gain / maintain and eat upto {bmrf} and to maintain eat atleast {bmr} '
            elif 21 <= body_fat_percentage < 25:
                bmrf=bmr-400
                return f'Focus on weight loss and maintain and eat atleast {bmrf} and to maintain eat atleast {bmr} and check  our 21 days plan'
            elif 25 <= body_fat_percentage < 32:
                bmrf=bmr-400
                return f'Focus on weight loss and eat atleast {bmrf} and check  our 21 days plan'
            else:
                bmrf=bmr-400
                return f'Primary Focus on weight loss and choose our 21 days plan eat atleast {bmrf}'
        elif gender == "Male":
            if body_fat_percentage < 6:
                bmrf=bmr+400
                return f'Focus on weight gain  and  eat upto {bmrf} '
            elif 6 <= body_fat_percentage < 14:
                bmrf=bmr+400
                return f'Focus on weight gain / maintain and eat upto {bmrf} and to maintain eat atleast {bmr}'
            elif 14 <= body_fat_percentage < 18:
                bmrf=bmr-400
                return f'Focus on weight loss and maintain and eat atleast {bmrf} and to maintain eat atleast {bmr} and check  our 21 days plan'
            elif 18 <= body_fat_percentage < 25:
                bmrf=bmr-400
                return f'Focus on weight loss and eat atleast {bmrf} and check  our 21 days plan'
            else:
                bmrf=bmr-400
                return f'Primary Focus on weight loss and choose our 21 days plan eat atleast {bmrf}'
        else:
            return ""
    


    if selected=="Predicting Bodyfat percent":
        st.header("Predicting your bodyfat percentage")
        gender = st.radio("Select your gender", ("Male", "Female"))
        name = st.text_input('Enter your name')
        uid=""
        uid=generate_id()
        uid=uid.upper()
        email = st.text_input('Enter your email')
        if email and not validate_email(email):
            st.warning('Please enter a valid email address')

        # Display email to user
        if email:
            st.success(f'Email entered: {email}')

        email=email.lower()
        Age = st.text_input("Enter your age:")
        if Age:
            Age = int(Age)
        
        Weight = st.text_input("Enter your weight in pounds: ")
        if Weight:
            Weight = float(Weight)
        
        Height = st.text_input("Enter your height in inches : ")
        if Height:
            Height = float(Height)
        
        Neck = st.text_input("Enter your neck in cm : ")
        if Neck:
            Neck = float(Neck)
        
        Chest = st.text_input("Enter your chest in cm : ")
        if Chest:
            Chest = float(Chest)
        
        Abdomen = st.text_input("Enter your abdomen in cm : ")
        if Abdomen:
            Abdomen = float(Abdomen)
        
        Hip = st.text_input("Enter your hip in cm : ")
        if Hip:
            Hip = float(Hip)
        
        
                
        if st.button('Calculate Body fat percentage'):
            bf2,bmi1,bf1,bmr1=bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip)
            st.write('Your Unique ID is (***SAVE THIS SOMEWHERE***) :',uid)
            st.write('Your Bodyfat percetage is :',round(bf2,2))
            st.write('Your BMI is :',round(bmi1,1))
            st.write('Your Bodyfat percetage according to BMI is :',round(bf1,2))
            st.write('Your BMR  is :',round(bmr1,2))
            insert_row(uid,gender, name,email, Age, Weight, Height, bmi1, bmr1, bf2, bf1)
            insert_row_ui(uid,name, email, Age, Weight, Height, Neck, Chest, Abdomen, Hip)
        
    if selected=="Your target Calories intake":
        conn = connect(credentials=credentials)
        
        
#AND email="{email}"
# Get user input for ID and email.
        email1 = st.text_input('Enter Email:')
        if email1 and not validate_email(email1):
            st.warning('Please enter a valid email address')

        # Display email to user
        if email1:
            st.success(f'Email entered: {email1}')
            email1=email1.lower()
        fitness_goal = st.radio("Select your fitness goal:", ("Weight Loss", "Weight Gain", "Weight Maintenance"))
        
        id1=st.text_input("Enter your UID number :",max_chars=8)
        error_msg2 = [
                    "INVALID-UID- What kind of fitness enthusiast you are that you cant remember your UID then how you gonna remember how much calories you ate",
                    "INVALID-UID- Looks like you're not just losing weight, you're also losing your memory!",
                    "INVALID-UID- I guess i'll have to work on toning those brain muscles before we tackle your body.",
                    "INVALID-UID- Let's hope you have a better handle on your calorie count than your UID.",
                    "INVALID-UID- Oh no, did you accidentally eat your UID for breakfast this morning?",
                    "INVALID-UID- If only losing weight was as easy as losing your UID!",
                    "INVALID-UID- Don't worry, we'll help you burn off those extra calories you consumed while searching for your UID.",
                    "INVALID-UID- Looks like someone needs a little more brain food to remember their UID!",
                    "INVALID-UID- Just remember, losing weight doesn't have to mean losing your mind (or your UID)!",
                    "INVALID-UID- If you can't remember your UID, I know you might know where you get best burger in town",
                    "INVALID-UID- I'm starting to think that your Invalid UID is my arch-nemesis.",
                    "INVALID-UID- I tried to use your Invalid UID as a password, but apparently it wasn't strong enough, it was mentioned its too easy",
                    "INVALID-UID- I think I need to hire a private investigator to help me find your Invalid UID, but still you don't remember it.",
                    "INVALID-UID- If I had a dollar for every time you entered an invalid UID, I'd be a millionaire by now.",
                    "INVALID-UID- This is frustating now it was just 8 digit number how can you cant remember 8 digit number do you know your contact number ?",
                    "INVALID-UID- I feel bad about forgetting your UID, just think of it as an opportunity to exercise your brain with some memory training exercises. just before training your body",
                    "INVALID-UID- We're sorry you're having trouble with your UID, but think of it this way, at least you're not a goldfish who forgets everything in 5 seconds.",
                    "INVALID-UID- Don't worry, we won't make you feel bad about forgetting your UID, that's what family and friends are for.",
                    "INVALID-UID- Ah, the classic case of UID amnesia. It's a common affliction, but thankfully there's a cure: writing things down.",
                    "INVALID-UID- Maybe you should try writing it down next time. You know, like we did in kindergarten."
                ]
        
        
        
        

# Run the SQL query and display the results.
        if st.button('Your target'):
                st.experimental_singleton
                def run_query(email1):
                   sheet_url = st.secrets["private_gsheets_url"]
                   rows = conn.execute(f'SELECT * FROM "{sheet_url}" WHERE email="{email1}"', headers=1)
                   rows = rows.fetchall()
                   return rows
                rows = run_query(email1)
                if len(rows) == 0:
                    st.warning('No results found. please check your body fat percentage first ')
                else:
                    df = DataFrame(rows, columns=['uid','gender','name', 'email', 'Age', 'Weight', 'Height', 'bmi', 'bmr', 'bodyfat', 'bf_bmi'])
                    bmr2=df.loc[0, 'bmr']
                    bmr2=round(bmr2,2)
                    name1=df.loc[0, 'name']
                    bodyfat1=df.loc[0, 'bodyfat']
                    gen=df.loc[0, 'gender']
                    # create radio button to select fitness goal
                    id1=id1.upper()
                    uid1=df.loc[0, 'uid']
                    ai_pred=classify_body_fat_percentage(gen,bodyfat1,bmr2)
                    if uid1==id1:# display selected fitness goal
                        if fitness_goal == "Weight Loss":
                            wl=bmr2-400
                            st.write("HEY! ",name1)
                            st.write("Your bodyfat Percentage is ",bodyfat1)
                            st.write("You have selected weight loss and your bmr is ",round(bmr2,2),"You have eat upto ",round(wl),"calories")
                            st.success(f'According to our AI : {name1} your aim should be {ai_pred}')
                        elif fitness_goal == "Weight Gain":
                            wg=bmr2+400
                            st.write("HEY! ",name1)
                            st.write("Your bodyfat Percentage is ",bodyfat1)
                            st.write("You have selected weight gain and your bmr is ",round(bmr2,2),"You have eat atleast ",round(wg),"calories")
                            st.success(f'According to our AI : {name1} your aim should be {ai_pred}')
                        else:
                            st.write("HEY! ",name1)
                            st.write("Your bodyfat Percentage is ",bodyfat1)
                            st.write("You have selected weight maintan and your bmr is ",round(bmr2,2),"You have eat exact ",round(bmr2,2),"calories")
                            st.success(f'According to our AI : {name1} your aim should be {ai_pred}')
                    else:
                        random_err = random.randint(0, len(error_msg2)-1)
                        st.warning(error_msg2[random_err])


    if selected=="21 days weight loss guide":
        
        conn = connect(credentials=credentials)
        st.experimental_singleton
        plans = st.radio("Select your workout goal:", ("30 mins", "45 mins", "60 mins"))
        exercise = st.radio("Whats your type of workout you plan to do  ", ("High intensity workout", "Low intensity workout", "Moderate intensity workout"))
        id1=st.text_input("Enter your UID number :",max_chars=8)
        email1 = st.text_input('Enter Email:')
        email1=email1.lower()
        
       
        def run_query(query):
            rows = conn.execute(query, headers=1)
            rows = rows.fetchall()
            return rows
        rows = run_query(f'SELECT * FROM "{sheet_url}" WHERE email="{email1}"')
        rows1 = run_query(f'SELECT * FROM "{sheet_url_ui}" WHERE email="{email1}"')
        
        if st.button('Your future'):
            
            
            
            if len(rows) & len(rows1) == 0:
                st.warning('No results found. please check your body fat percentage first ')
            else:
                df1 = DataFrame(rows1, columns=['uid','name','email','age','weight','height','neck','chest','abdomen','hip'])
                df = DataFrame(rows, columns=['uid','gender', 'name', 'email', 'Age', 'Weight', 'Height', 'bmi', 'bmr', 'bodyfat', 'bf_bmi'])
                bmr3=df.loc[0, 'bmr']
                name1=df.loc[0, 'name']
                bodyfat1=df.loc[0, 'bodyfat']
                gen=df.loc[0, 'gender']
                neck=df1.loc[0, 'neck']
                chest=df1.loc[0, 'chest']
                abdomen=df1.loc[0, 'abdomen']
                hip=df1.loc[0, 'hip']
                age= df.loc[0, 'Age']
                height=df.loc[0, 'Height']


                starting_weight = df.loc[0, 'Weight']
                starting_weight=starting_weight/2.205# pounds
            if plans == "30 mins":
                if exercise == "High intensity workout":
                    met=8.5
                elif exercise == "Low intensity workout":
                    met=3
                else:
                    met=4.5
                time_hours = 30 / 60  
                wl=bmr3-400
                daily_calories = wl
                    # calories/day
                exercise_calories = met * starting_weight * time_hours
            elif plans == "45 mins":
                if exercise == "High intensity workout":
                    met=8.5
                elif exercise == "Low intensity workout":
                    met=3
                else:
                    met=4.5
                time_hours = 45 / 60    
                exercise_calories = met * starting_weight * time_hours
                wl=bmr3-400
                daily_calories = wl
            else: 
                if exercise == "High intensity workout":
                    met=8.5
                elif exercise == "Low intensity workout":
                    met=3
                else:
                    met=4.5
                time_hours = 60 / 60    
                exercise_calories = met * starting_weight * time_hours
                wl=bmr3-400
                daily_calories = wl
            daily_steps = 10000
            days = 21
            # Calculate daily calorie expenditure
            def calculate_daily_calories(bmr3, daily_calories, exercise_calories, daily_steps):
                return bmr3 + (exercise_calories) + (daily_steps * 0.05)
            daily_calorie_expenditure = calculate_daily_calories(bmr3, daily_calories, exercise_calories, daily_steps)

            # Calculate daily calorie deficit
            daily_calorie_deficit = daily_calorie_expenditure - daily_calories
                                    
            # Calculate daily weight loss
            daily_weight_loss = daily_calorie_deficit / 3500  # 1 pound of fat is approximately 3500 calories

            # Create a dataframe to store the daily weight and day number
            weight_data = {'Day': range(1, days+1)}
            weight_df = pd.DataFrame(weight_data)

            # Calculate the estimated weight for each day
            weight_df['Weight'] = starting_weight - (daily_weight_loss * weight_df['Day'])
            

            # Plot the estimated weight loss over time using Seaborn
            

            # Calculate final weight
            final_weight = weight_df.iloc[-1]['Weight']
            id1=id1.upper()
            uid1=df.loc[0, 'uid']
            error_msg = [
                        "INVALID-UID- I'm starting to think that your Invalid UID is my arch-nemesis.",
                        "INVALID-UID- I tried to use your Invalid UID as a password, but apparently it wasn't strong enough, it was mentioned its too easy",
                        "INVALID-UID- I think I need to hire a private investigator to help me find your Invalid UID, but still you don't remember it.",
                        "INVALID-UID- If I had a dollar for every time you entered an invalid UID, I'd be a millionaire by now.",
                        "INVALID-UID- This is frustating now it was just 8 digit number how can you cant remember 8 digit number do you know your contact number ?",
                        "INVALID-UID- I feel bad about forgetting your UID, just think of it as an opportunity to exercise your brain with some memory training exercises. just before training your body",
                        "INVALID-UID- We're sorry you're having trouble with your UID, but think of it this way, at least you're not a goldfish who forgets everything in 5 seconds.",
                        "INVALID-UID- Don't worry, we won't make you feel bad about forgetting your UID, that's what family and friends are for.",
                        "INVALID-UID- Ah, the classic case of UID amnesia. It's a common affliction, but thankfully there's a cure: writing things down.",
                        "INVALID-UID- Maybe you should try writing it down next time. You know, like we did in kindergarten."
                        "INVALID-UID- What kind of fitness enthusiast you are that you cant remember your UID then how you gonna remember how much calories you ate",
                        "INVALID-UID- Looks like you're not just losing weight, you're also losing your memory!",
                        "INVALID-UID- I guess i'll have to work on toning those brain muscles before we tackle your body.",
                        "INVALID-UID- Let's hope you have a better handle on your calorie count than your UID.",
                        "INVALID-UID- Oh no, did you accidentally eat your UID for breakfast this morning?",
                        "INVALID-UID- If only losing weight was as easy as losing your UID!",
                        "INVALID-UID- Don't worry, we'll help you burn off those extra calories you consumed while searching for your UID.",
                        "INVALID-UID- Looks like someone needs a little more brain food to remember their UID!",
                        "INVALID-UID- Just remember, losing weight doesn't have to mean losing your mind (or your UID)!",
                        "INVALID-UID- If you can't remember your UID, I know you might know where you get best burger in town",
                    ]

            if uid1==id1:
                text = f"HEY! {name1} Your present weight is {round(starting_weight,2)} kgs and final weight after 21 days according to our plan would be {round(final_weight,2)} kgs\n"
                text += f"So {name1}, your bodyfat Percentage is {bodyfat1}\n"
                text += f"For results like this you have to walk at least {daily_steps} steps daily and do {exercise} for {plans} daily\n"
                text += f"This will lead you to burn {daily_steps * 0.05} calories from {daily_steps} steps and by {exercise} for {plans} you will burn {round(exercise_calories,2)} calories\n"
                text += f"YOUR DAILY CALORIE EXPENDITURE WOULD BE : {daily_calorie_deficit}\n"
                text += f"If you wanna lose {round(round(starting_weight,2)-round(final_weight,2),2)} kgs Read our Weight loss ebook which is completely free for now\n"
                text += f"1:- In this ebook you will learn what Kind of workouts should do in {exercise}\n"
                text += f"2:- Plus you will also get insights what should be your diet according to your calories i.e. {round(wl,0)}"

                                
                st.write("HEY! ",name1,"Your present weight is ",round(starting_weight,2)," kgs and final weight after 21 days according to our plan would be " ,round(final_weight,2) ,"kgs")
                st.write("***REPORT***")
                st.write("So ",name1," your bodyfat Percentage is ",bodyfat1)
                st.write("For results like this you have to walk altleats ",daily_steps," steps daily and do ",exercise,"for ",plans," daily")
                st.write("This will lead you to burn ",(daily_steps * 0.05)," calories"," from ",daily_steps," steps and by ",exercise,"for ",plans," you will burn ",round(exercise_calories,2)," calories")
                st.write("***YOUR DAILY CALORIE EXPENDITURE WOULD BE*** :",daily_calorie_deficit )
                st.write("If you wanna lose ",round(round(starting_weight,2)-round(final_weight,2),2)," kgs Read our Weight loss ebook which is completely free for now")
                st.write("1:- ***In this ebook you will learn what Kind of workouts shoul do in***",exercise)
                st.write("2:- ***Plus you will also get insights what should be your diet according to your calories i.e.*** ",round(wl,0))
                link = "<a href='https://www.dietncity.com' target='_blank'>FREE EBOOK</a>"
                st.write("Click the link below")
                st.markdown(link, unsafe_allow_html=True)
                pdf = PDF()
                pdf.add_page()
                pdf.body_composition(uid1,name1,age, starting_weight, height, bodyfat1,bmr3,neck,chest,abdomen,hip,text)
                pdf_file_path = f'{name1}_body_composition.pdf'
                pdf.output(pdf_file_path, 'F')
                st.success('PDF file exported successfully!')
                with open(pdf_file_path, 'rb') as f:
                    pdf_data = f.read()
                st.download_button('Download PDF', data=pdf_data, file_name=f'{name1}_body_composition.pdf', mime='application/pdf')
            else:
                random_err = random.randint(0, len(error_msg)-1)

                st.error(error_msg[random_err])
    
            
            
           
            
                
                
                
                
                        

if __name__=='__main__': 
    main()
