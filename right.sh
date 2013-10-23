#!/bin/bash
chown sschat:sschat ./*
chown sschat:sschat .
chown key:key key

chmod 501 .
chmod 500 key
chmod 500 .ssh

chmod 600 *.pyc
chmod 600 bugReport
chmod 400 *.py
chmod 400 mot*
chmod 400 README.md
chmod u+x wrapper.py

chmod 500 key/key*
chmod 400 key/text.py
chmod 600 key/*.pyc
chmod 400 key/.hushlogin
