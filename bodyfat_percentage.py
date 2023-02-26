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
import uuid
from sklearn.linear_model import LinearRegression
import mysql.connector
import time
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

    @st.cache_resource
    def init_connection():
        return mysql.connector.connect(**st.secrets["mysql"])

    conn = init_connection()
    # Perform query.
    @st.cache_data(ttl=100)
    def insert_data(uid, Age, Weight, Height, bmi1, bmr1, bf2, bf1):
    # Initialize the database connection
        conn = init_connection()

    # Define the SQL query to insert the data
        sql_query = "INSERT INTO user_input (id, email, Age, Weight, Height, bmi, bmr, bodyfat, bf_bmi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (uid, email, Age, Weight, Height, bmi1, bmr1, bf2, bf1)

    # Execute the query to insert the data
        mycursor = conn.cursor()
        mycursor.execute(sql_query, data)
        conn.commit()

    # Return a success message
        return "Data inserted successfully!"
    

    mycursor=conn.cursor()
    def validate_email(email):
        # A simple regex to validate email format
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    if selected=="Predicting Bodyfat percent":
        import random
        import string

        def generate_student_id():
            alphanumeric = string.ascii_uppercase + string.digits
            student_id = ''.join(random.choices(alphanumeric, k=5))
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

        Age=st.number_input("Enter your age:", value=0, format="%d")
        Weight=st.number_input("Enter your weight in pounds: ", format="%.1f")
        Height=st.number_input("Enter your height in inches : ", format="%.1f")
        Neck=st.number_input("Enter your neck in cm : ", format="%.1f")
        Chest=st.number_input("Enter your chest in cm : ", format="%.1f")
        Abdomen=st.number_input("Enter your abdomen in cm : ", format="%.1f")
        Hip=st.number_input("Enter your hip in cm : ", format="%.1f")
        Thigh=st.number_input("Enter your thigh in cm : ", format="%.1f")
        Knee=st.number_input("Enter your knee in cm : ", format="%.1f")
        Ankle=st.number_input("Enter your ankle in cm : ", format="%.1f")
        Biceps=st.number_input("Enter your biceps in cm : ", format="%.1f")
        Forearm=st.number_input("Enter your forearm in cm : ", format="%.1f")
        Wrist=st.number_input("Enter your wrist in cm : ", format="%.1f")
        
        if st.button('Calculate Body fat percentage'):
            bf2,bmi1,bf1,bmr1=bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist)
            st.write('Your Bodyfat percetage is :',round(bf2,2))
            st.write('Your BMI is :',round(bmi1,1))
            st.write('Your Bodyfat percetage according to BMI is :',round(bf1,2))
            st.write('Your BMR  is :',round(bmr1,2))
            insert_data(uid,email, Age, Weight, Height, bmi1, bmr1, bf2, bf1)
            

        #bmr2=bmr1
        
    #if selected=="Best suitable diet for you":
        #bmr2=bmr1
        # create radio button to select fitness goal
        #fitness_goal = st.radio("Select your fitness goal:", ("Weight Loss", "Weight Gain", "Weight Maintenance"))
        # display selected fitness goal
        #if fitness_goal == "Weight Loss":
         #   wl=bmr2-300
          #  st.write("You have selected weight loss and your bmr is ",round(bmr2,2),"You have eat upto ",wl)
        #elif fitness_goal == "Weight Gain":
         #  wg=bmr2-300
          # st.write("You have selected weight gain and your bmr is ",round(bmr2,2),"You have eat atleast ",wg)
        #else:
         #   st.write("You have selected weight maintan and your bmr is ",round(bmr2,2),"You have eat exact ",round(bmr2,2))
if __name__=='__main__': 
    main()
