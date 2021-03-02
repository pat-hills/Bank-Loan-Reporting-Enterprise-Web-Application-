import datetime

def greetings():
    currentTime = datetime.datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
     greet = 'Good morning'
    elif 12 <= currentTime.hour < 18:
     greet = 'Good afternoon'
    else:
      greet = 'Good evening'

    return greet