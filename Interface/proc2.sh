#!/bin/bash

X=0
while [ ${X} -eq 0 ]
do
	proc2_state=$(ps -ef | grep "proc1.sh" | grep -v grep | wc -l | xargs)
	if [ ${proc2_state} -eq 0 ]; then
		echo "Process stop running"
		/bin/bash proc1.sh &
	else
		echo "Process running"
	fi
done
