from datetime import datetime, date

#Gets the stripped birthdate and calculates the age based on the current date 
def update_age(birthdate):
    today_date = date.today()                                                         #Current Date
    return today_date.year - birthdate.year - ( (today_date.month, today_date.day)    #Calculates the age based on the current date and stripped birthday
    < (birthdate.month, birthdate.day) ) 