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

    print('*'*30, str(now), '*'*30)
    print(time)
    print(weekday)

    with open('log/' +str(time) + '.txt', 'w') as f: 
        f.write('')
    
    if weekday < 5:
        if time > datetime.time(15,30):
            with open('log/running.txt', 'w') as f:
                f.write('runing')
            print('sh run4.bash')
            os.system('sh run4.bash')
            sleep(A_DAY)
        else:
            sleep(FIVE_MIN)
    else:
        sleep(A_DAY)

