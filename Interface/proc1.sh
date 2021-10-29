#!/bin/bash
python interface.py &

X=0
while [ ${X} -eq 0 ]
do
	proc2_state=$(ps -ef | grep "proc2.sh" | grep -v grep | wc -l | xargs)	
	interface_state=$(ps -ef | grep "interface.py" | grep -v grep | wc -l | xargs)
	if [ ${proc2_state} -eq 0 ]; then
		echo "Process stop running"
		/bin/bash proc2.sh &
		
	elif [ ${interface_state} -eq 0 ]; then
		python interface.py &
		
	else
		echo "Process running"
	fi
done
