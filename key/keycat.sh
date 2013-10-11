#!/bin/bash
if [[ $1 == '1' ]]
then
line="ssh-rsa "$2
elif [[ $1 == '2' ]]
then
line="ssh-dss "$2
else
exit
fi
echo "$line" >> /sschat/.ssh/authorized_keys
