linuxHelp=["On your computer, enter the following commands:",
"ssh-keygen -t rsa -b 2048",
"cat ~/.ssh/id_rsa.pub",
"Copy the result from the previous command.",
"Come back here and paste it."]

windowsHelp=["If you use Putty, you'll need puttygen :",
"http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html",
"\nGenerate a new key pair.",
"Copy your one-line public-key from the central box.",
"(It begins with ssh-rsa)",
"Save your private-key on a file (and hide it).",
"Come back here and paste your public-key.",
"\nOpen Putty.",
"Create a new profile",
"Fill the Host and Port field.",
"In Connexion -> Data : fill Auto-login username with sschat.",
"In SSH -> Auth : click on Browse and choose your private key.",
"Save the changes.",
"You are done."]

androidHelp=["You can do all the operations on an android device.",
"ConnectBot allows you to create your key pair, and register it here.",
"https://play.google.com/store/apps/details?id=org.connectbot"]

ask=["Paste your one-line ssh publikey (RSA 2048 bits or DSA):",
"Something like ssh-rsa AAAAB3N... or ssh-dss AAAAB3N...",
"If you need help, type help. / Ctrl+c to quit."]

congrats=["\nCongratulations!",
"You can now connect to the user sschat.",
"For now, you'll most likely find people in the channel : plop ",
"\n\nNote that this server will not keep any trace of anything but your publikey.",
"Please remember that this service comes with NO FUCKING GUARANTEE",
"\nEnter to quit."]

def printer(text):
	print " "
        for line in text:
                        print line
	print " "
