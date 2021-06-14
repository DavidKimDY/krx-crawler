import datetime
import os 

if datetime.datetime.now().astimezone().tzname() == 'KST':
	print('KST')
else:
	os.system('sh timezone.bash')
