# Code/Art Future LeadHERS Project - Database Git 

## Group: Alexandra Fernandez & Isabelle Rivera

## Overview of Project: 
The goal of the Code/Art LEADHers project is to create an iOS application for young female students who are a part of Code/Art’s Future Tech LeadHERS program. Code/Art is a nonprofit organization aimed at getting more girls into the computer science field. Hence, this application, along with the database and administrative dashboard, is aimed to help keep female students engaged in Computer Science in the middle school and high school years. This application includes account creation and login where a student will be able to view events and internships that are being hosted by Code/Art or one of their partners. The administrative dashboard will be accessed only on a desktop or laptop where admins can create, modify, or delete these events and internships. In addition, they can easily remove, modify, or create user or admin accounts. Thus, this project provides security and ease of use to its users and its administrators. 

## Implemented Features: 
1. Admin Login with Error check and displayed Error message (omits whether email or password was wrong for security purposes)
2. Communication with app for sign up and login 
3. Admin Dashboard with Account, Internship, and Event menus and information displayed
4. Create, Edit, and Modify functions in admin dashboard for all menus
5. Calculates age of the user based on the birthday input  
6. Logout Functionality
7. Only logged in and verified admins can view the dashboard 

## Not Yet Implemented Features: 
1. App communication in the profile, internships, and events
2. Confirmation and Forgot Password emails 
3. Signin and Admin Dashboard HTML does not yet match CodeArt brand, colors, and font

## Dependencies: 
1. Python 3.8.5
2. Flask and its respective imports, such as flask_login -- Flask 1.1.2
3. SQLAlchemy 1.1
4. Werkzeug 1.0.1

## Instructions for Compilation
1. Download the project via git / or zip
2. Open folder
3. pip install -r requirements.txt
4. python /initialization/init_db.py
5. (For any new admins or if the database is entirely reset) python /initialization/admin_credentials.py

## Instructions for Running
1. python -m flask run --port 4258 (Change the port based on the port that you want listened in on)
    i. This needs to run in the background constantly so ' screen -r ' without the quotes will be needed to create a background screen so that, when this previous command is used, the database will always be running

