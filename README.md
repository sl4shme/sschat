Ss(c)h(at)
===================
```
    c
s s h is a no-Log, IRC type, ssh securised, chat.  
    a
    t
```
### INSTALL


First, clone or download sschat:

```
git clone https://github.com/sl4shme/sschat.git
```

Then to install, just create those users:
- One to add any key with key.py as shell
- One to connect to the chat with wrapper.py as shell 

Don't forget to change directories to match your setup.

```bash
cat /etc/passwd
...
sschat:x:1000:1000:,,,:/sschat:/sschat/wrapper.py  
key:x:1001:1001:,,,:/sschat/key:/sschat/key/key.py  
...
```

Next, add this line to /etc/sudoers (Yep, you need sudo):

```
key ALL=(ALL) NOPASSWD: /sschat/key/keycat.sh
```


Modify your /etc/ssh/sshd_config:

```
match user sschat
PasswordAuthentication no
PubkeyAuthentication yes
```

Permissions of your installation directory should match those ones :
```
dr-x-----x  6 sschat sschat .
drwxr-xr-x 24 root   root   ..
drwxr-xr-x  8 root   root   .git
-r--------  1 sschat sschat .hushlogin
dr-x------  2 sschat sschat .ssh
-r--------  1 sschat sschat README.md
-rw-------  1 sschat sschat bugReport
-r--------  1 sschat sschat crypt.py
-rw-------  1 sschat sschat crypt.pyc
dr-x------  2 key    key    key
-r--------  1 sschat sschat minion.py
-rw-------  1 sschat sschat minion.pyc
-r--------  1 sschat sschat motb
-r--------  1 sschat sschat motd
-r-x------  1 sschat sschat right.sh
-r--------  1 sschat sschat screen.py
-rw-------  1 sschat sschat screen.pyc
-r--------  1 sschat sschat scroll.py
-rw-------  1 sschat sschat scroll.pyc
-r--------  1 sschat sschat sschat.py
-rw-------  1 sschat sschat sschat.pyc
-r--------  1 sschat sschat text.py
-rw-------  1 sschat sschat text.pyc
-rwx------  1 root   root   updater.py
-r-x------  1 sschat sschat wrapper.py
```

right.sh can help you here.


### USAGE

Connect with ssh on your server with key as the user.
Paste your 2048 bits RSA / 1024 Bits DSA SSH publikey.

Connect with ssh on your server with sschat as the user.
Here you are!


### COMMANDS

```
/help : Display this help, use j/k to navigate and q to quit.
/list : List peoples in channel.
/clear : Clear your screen.
/paste : Enter paste mode, usefull for pasting long links.
/me : That's you.
/quit [message] : Quit with an optional [message].
/history [on|off|clear] : With no argument, display the last 100 message.
/nickname <newNickname> : Change your nickname.
/channel <newChannelName> : Switch channel.
/pm <id> <message> : Send a private message to the user with the id <id>
/bug <message> : Send a bug / suggestion report.
/timestamp <on|off> : Enable/disable line timestamping.
/notif <on|off> : Toggle visual flash notification on new message.
/afk : Toggle afk.
/encrypt <on|off> : Toggle encryption.
```
