from datetime import datetime, date

def update_age(birthdate):
    today_date = date.today()
    return today_date.year - birthdate.year - ( (today_date.month, today_date.day) 
    < (birthdate.month, birthdate.day) ) 