import datetime
import os
from time import sleep

os.system('python3 timezone.py')

while True:
    now = datetime.datetime.now()
    time = now.time()
    weekday = now.weekday()

    A_HOUR = 60 * 60
    FIVE_MIN = 60 * 5
    A_DAY = A_HOUR * 24

    if weekday < 5:
        if time > datetime.time(15,30):
            os.system('sh run4.bash')
            sleep(A_DAY)
        else:
            sleep(FIVE_MIN)
    else:
        sleep(A_DAY)

