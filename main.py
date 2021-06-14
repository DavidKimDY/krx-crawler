import datetime
import time
import os


now = datetime.datetime.now()
time = now.time()
weekday = now.weekday()

A_HOUR = 60 * 60
A_DAY = A_HOUR * 24

print(time)
print(weekday)

os.system('python3 timezone.py')

if weekday < 5:
    if time > datetime.time(15,30):
        print('sh run4.bash')
        os.system('sh run4.bash')
    else:
        time.sleep(A_HOUR)
else:
    time.sleep(A_DAY)
