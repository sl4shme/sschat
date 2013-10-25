import re

def validateName(input):
	if re.match("^\d*[a-zA-Z][a-zA-Z\d]*$", input) and len(input) <= 12:
        	return True
	else :
		return False

def getSpawnLock():
        while 1:
                if "OK" in open("lock"):
                        f = open("lock", 'w')
                        f.write("KO")
                        f.close()
                        return

def releaseSpawnLock():
        f = open("lock", 'w')
        f.write("OK")
        f.close()

