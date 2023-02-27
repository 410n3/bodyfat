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



den=pickle.load(open("den_pred.sav",'rb'))
bfper=pickle.load(open("bf_pred.sav",'rb'))

def bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist):
    # Calculating body fat percentage for males
    height=float(Height)
    height=height*2.54
    weight=float(Weight)
    weight=weight*2.205
    body_fat_perc=0
    bmr=0
    if gender == "Male":
        body_fat_perc= 495 / (1.0324 - 0.19077 * (math.log10(Abdomen - Neck)) + 0.15456 * (math.log10(height))) - 450
        bmr = (3.397*weight)+ (4.799*height) - (5.677*Age) + 88.362
# Calculating body fat percentage for females
    elif gender == "Female":
        body_fat_perc = 495 / (1.29579 - 0.35004 * (math.log10(Abdomen + Hip - Neck)) + 0.22100 * (math.log10(Height))) - 450
        bmr=(9.247*weight) + (3.098*height) - (4.330*Age) + 447.593
    else:
        return "Invalid input. Please enter M or F for gender."
    user_update=[[body_fat_perc,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist]]
    prediction=den.predict(user_update)
    user_update2=[[prediction[0],Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist]]
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
        bf1=round(prediction2[0],3)
        return bf1,bmi,bf,bmr
            
    elif bmi <= 29.9:  
            if bf > prediction2[0]:  
                conclusion = bf - prediction2[0]
                conclusion = round(conclusion, 0)
                bf1=round(prediction2[0] + conclusion,3)
                return bf1,bmi,bf,bmr
            else:
                conclusion = prediction2[0]-bf
                conclusion = round(conclusion, 0)
                bf1=round(prediction2[0] + conclusion,3)
                return bf1,bmi,bf,bmr
    else:  
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
def main():
    page_title="AI Bodyfat percentage calculator"
    page_icon=":chart_with_downwards_trend:"
    st.set_page_config(page_title=page_title,page_icon=page_icon)
    st.markdown(""" <style> #MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
    st.title(page_icon + " " + page_title)
    selected=option_menu( 
        menu_title=None,
        options=["Predicting Bodyfat percent","Best suitable diet for you"],
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

    # Insert a row into the Google Sheet.
    def insert_row(uid, email, Age, Weight, Height, bmi1, bmr1, bf2, bf1):
        row = [uid, email, Age, Weight, Height, bmi1, bmr1, bf2, bf1]
        sheet.insert_row(row, 2)  # Insert the row at the second row (after the header).
        st.success('Data inserted successfully.')
        ###
    def validate_email(email):
        # A simple regex to validate email format
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    if selected=="Predicting Bodyfat percent":
        import random
        import string

        def generate_student_id():
            alphanumeric = string.ascii_uppercase + string.digits
            student_id = ''.join(random.choices(alphanumeric, k=8))
            return student_id
        uid=generate_student_id()
        st.header("Predicting your bodyfat percentage")
        gender = st.radio("Select your gender", ("Male", "Female"))
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
        
        Thigh = st.text_input("Enter your thigh in cm : ")
        if Thigh:
            Thigh = float(Thigh)
        
        Knee = st.text_input("Enter your knee in cm : ")
        if Knee:
            Knee = float(Knee)
        
        Ankle = st.text_input("Enter your ankle in cm : ")
        if Ankle:
            Ankle = float(Ankle)
        
        Biceps = st.text_input("Enter your biceps in cm : ")
        if Biceps:
            Biceps = float(Biceps)
        
        Forearm = st.text_input("Enter your forearm in cm : ")
        if Forearm:
            Forearm = float(Forearm)
        
        Wrist = st.text_input("Enter your wrist in cm : ")
        if Wrist:
            Wrist = float(Wrist)
        
                
        if st.button('Calculate Body fat percentage'):
            bf2,bmi1,bf1,bmr1=bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist)
            st.write('Your Bodyfat percetage is :',round(bf2,2))
            st.write('Your BMI is :',round(bmi1,1))
            st.write('Your Bodyfat percetage according to BMI is :',round(bf1,2))
            st.write('Your BMR  is :',round(bmr1,2))
            insert_row(uid,email, Age, Weight, Height, bmi1, bmr1, bf2, bf1)
        
    if selected=="Best suitable diet for you":
        conn = connect(credentials=credentials)
        st.experimental_singleton
        def run_query(email):
            sheet_url = st.secrets["private_gsheets_url"]
            rows = conn.execute(f'SELECT * FROM "{sheet_url}" WHERE email="{email}"', headers=1)
            rows = rows.fetchall()
            return rows
#AND email="{email}"
# Get user input for ID and email.
        id1 = st.text_input('Enter UID you recieved on your email :')
        fitness_goal = st.radio("Select your fitness goal:", ("Weight Loss", "Weight Gain", "Weight Maintenance"))
        email1 = st.text_input('Enter Email:')
        email1=email1.lower()
        id1=id1.upper()
        

# Run the SQL query and display the results.
        if st.button('Your target'):
            rows = run_query(email1)
            if len(rows) == 0:
                st.warning('No results found.')
            else:
                df = DataFrame(rows, columns=['id', 'email', 'Age', 'Weight', 'Height', 'bmi', 'bmr', 'bodyfat', 'bf_bmi'])
                bmr2=df.loc[0, 'bmr']
                # create radio button to select fitness goal
                
                # display selected fitness goal
                if fitness_goal == "Weight Loss":
                    wl=bmr2-400
                    st.write("You have selected weight loss and your bmr is ",round(bmr2,2),"You have eat upto ",round(wl))
                elif fitness_goal == "Weight Gain":
                    wg=bmr2+400
                    st.write("You have selected weight gain and your bmr is ",round(bmr2,2),"You have eat atleast ",round(wg))
                else:
                    st.write("You have selected weight maintan and your bmr is ",round(bmr2,2),"You have eat exact ",round(bmr2,2))





if __name__=='__main__': 
    main()
