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
den=pickle.load(open("den_pred.sav",'rb'))
bfper=pickle.load(open("bf_pred.sav",'rb'))
def bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist):
    # Calculating body fat percentage for males
    height=float(Height)
    height=height*2.54
    body_fat_perc=0
    if gender == "Male":
        body_fat_perc= 495 / (1.0324 - 0.19077 * (math.log10(Abdomen - Neck)) + 0.15456 * (math.log10(height))) - 450

# Calculating body fat percentage for females
    elif gender == "Female":
        body_fat_perc = 495 / (1.29579 - 0.35004 * (math.log10(Abdomen + Hip - Neck)) + 0.22100 * (math.log10(Height))) - 450

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
            return "Body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf)
        else:
            conclusion = prediction2[0] - bf
            conclusion = round(conclusion, 0)
            return "Body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf)
    elif bmi <= 24.9:  
            return "Body fat % is ", round(prediction2[0],3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf)
    elif bmi <= 29.9:  
            if bf > prediction2[0]:  
                conclusion = bf - prediction2[0]
                conclusion = round(conclusion, 0)
                return "body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf),"Bodyfat % according to US-Navy: ",body_fat_perc
            else:
                conclusion = prediction2[0]-bf
                conclusion = round(conclusion, 0)
                return "body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf),"Bodyfat % according to US-Navy: ",body_fat_perc
    else:  
                if bf > prediction2[0]:  
                    conclusion = bf - prediction2[0]
                    conclusion = round(conclusion, 0)
                    return "body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf)
                else:
                    conclusion = prediction2[0] - bf
                    conclusion = round(conclusion, 0)
                    return "body fat % is ", round(prediction2[0] + conclusion,3),"Your BMI is :",round(bmi,2),"Bodyfat % according to BMI is : ", round(bf)
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
    if selected=="Predicting Bodyfat percent":
        id=uuid.uuid4()
        id=id.time
        st.header("Predicting your bodyfat percentage")
        gender = st.radio("Select your gender", ("Male", "Female"))
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
        
        userinput=''
        if st.button('Calculate Body fat percentage'):
            userinput=bodyfat(gender,Age,Weight,Height,Neck,Chest,Abdomen,Hip,Thigh,Knee,Ankle,Biceps,Forearm,Wrist)
        st.success(userinput)
    #if selected=="Best suitable diet for you";
        #ask adi

if __name__=='__main__': 
    main()
