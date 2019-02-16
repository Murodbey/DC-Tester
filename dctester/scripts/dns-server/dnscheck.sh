#!/bin/bash 
#!/bin/bash

ipaddr=$(cat scripts/info.txt | awk '{print $1}')
dnsname=$(cat scripts/info.txt | awk '{print $2}')
checkhost=$(ping -c 1 $ipaddr &> /dev/null && echo success || echo fail)
if [ $checkhost == "success" ]
then
	echo "$(echo "nameserver $ipaddr" | cat - /etc/resolv.conf)" >  /etc/resolv.conf
	checkname=$(ping -c 1 $dnsname &> /dev/null && echo success || echo fail)
	if [ $checkname == "success" ]
	then
		echo "DONE"
	else
		echo "DOWN"
	fi	
	
else
	echo "DOWN"
fi


sed "/$ipaddr/d" -i /etc/resolv.conf &> /dev/null
