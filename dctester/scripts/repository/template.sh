#!/bin/bash

OSS=$(cat /etc/redhat-release | grep -oh '7\|6' | head -n1| grep -v ^$)
ipaddr=$(ip route get 8.8.8.8 | awk 'NR==1 {print $NF}')

#This line will check vsftpd installed or not
vsftpdcheck=$(rpm -qa | grep -o vsftpd) 
if [ $vsftpdcheck == "vsftpd" ] &> /dev/null
then
	echo "installed" &> /dev/null 
else
	echo "FALSE" 
	mv /etc/yum.repos/old/* /etc/yum.repos/  &> /dev/null
	rm -rf /etc/yum.repos/old/ &> /dev/null
	exit 1
fi

# This line looking for the line for
findresult=$(find /var/ftp/ -name "RPM-GPG-KEY-CentOS-Debug-6" | sed  "s/RPM-GPG-KEY-CentOS-Debug-6//g" | cut -c9-) &> /dev/null
sed "s|folder|$findresult|g" -i /etc/yum.repos.d/template.repo &> /dev/null
yum erase tree -y &> /dev/null
yum install tree -y &> /dev/null
# This line will check tree command
trees=$(rpm -qa | grep -o tree) &> /dev/null
if [ $trees == "tree" ]  &> /dev/null
then
	echo "DONE" 
else
	echo "FALSE" 
fi
mv /etc/yum.repos/old/* /etc/yum.repos/  &> /dev/null
rm -rf /etc/yum.repos/old/ &> /dev/null
