export PID=$(ps aux | grep -v awk |awk /not_db/'{print $2}')
echo killing $PID
echo $PID >/tmp/PID
