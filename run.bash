python3 stock_list.py
input="stock_list.txt"
count=0
process=5

while IFS= read -r line
do
	if [ ${count} -ne ${process} ] ; then
		python3 krx_data_update.py "$line" &
		count=`expr $count + 1`
	elif [ ${count} -eq ${process} ] ; then
		python3 krx_data_update.py "$line" 
		count=0
	fi
done < "$input"

python3 save_into_mongodb.py

