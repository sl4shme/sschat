ss(c)h(at)  
No-Log, IRC type, ssh securised, chat.  


/etc/passwd  

sschat:x:1000:1000:,,,:/sschat:/sschat/sschat.py  
key:x:1001:1001:,,,:/sschat/key:/sschat/key/key.py  



/etc/sudoers  

key ALL=(ALL) NOPASSWD: /sschat/key/keycat.sh  



ls /sschat/  

bugReport  
crypt.py  
crypt.pyc  
.hushlogin  
key  
     .hushlogin  
     keycat.sh  
     key.py   
     text.py  
     text.pyc  
minion.py  
minion.pyc  
motb  
motd  
screen.py  
screen.pyc  
scroll.py  
scroll.pyc  
sschat.py  
.ssh  
     authorized_keys  
text.py  
text.pyc  
TODO  
