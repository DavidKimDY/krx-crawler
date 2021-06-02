for f in `ls krx_data_test`
do
python krx_data_update.py "$f"
done
