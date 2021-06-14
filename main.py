import datetime
import time
import os


now = datetime.datetime.now()
time = now.time()
weekday = now.weekday()

a_hour = 60 * 60
a_day = a_hour * 24

print(time)
print(weekday)

os.system('python3 timezone.py')

if weekday < 5:
    if time > datetime.time(15,30):
        print('sh run4.bash')  
        os.system('sh run4.bash')
    else:
        time.sleep(a_hour) 
         
else:
    time.sleep(a_day)      
