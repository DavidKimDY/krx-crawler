count=1
while [ $count -le 100000 ] 
do
	flag=`expr $count % 5`
	if [ $flag -ne  0 ] ; then
		python3 total_crawler.py $count &
	else		
		python3 total_crawler.py $count
	fi
	count=`expr $count  + 1`
done
