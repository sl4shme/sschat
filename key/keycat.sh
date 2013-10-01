#!/bin/bash
line="ssh-rsa "$1
echo "$line" >> /sschat/.ssh/authorized_keys
