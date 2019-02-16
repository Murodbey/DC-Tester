#!/bin/bash

ipaddr=$(cat scripts/info.txt | awk '{print $1}')
checkhost=$(ping -c 1 $ipaddr &> /dev/null && echo success || echo fail)
if [ $checkhost == "success" ]
then
	ssh root@$ipaddr "ls"  &> /dev/null && echo "" &> /dev/null || echo "ERROR"
	cp scripts/repository/template scripts/repository/template.repo &> /dev/null
	ssh root@$ipaddr "mkdir  /etc/yum.repos.d/old " &> /dev/null
	ssh root@$ipaddr "mv /etc/yum.repos.d/* /etc/yum.repos.d/old/ " &> /dev/null
	sed -i  "s|IPADDR|$ipaddr|g"   scripts/repository/template.repo &> /dev/null
	scp scripts/repository/template.repo  root@$ipaddr:/etc/yum.repos.d/
	rm -rf scripts/repository/template.repo &> /dev/null
	ssh root@$ipaddr "bash -s " < scripts/repository/template.sh
	ssh root@$ipaddr "mv /etc/yum.repos.d/old/* /etc/yum.repos.d/" &> /dev/null
	ssh root@$ipaddr "rm -rf /etc/yum.repos.d/template.repo" &> /dev/null
else
	echo "DOWN"
fi
