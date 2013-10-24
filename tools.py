import re

def validateName(input):
	if re.match("^\d*[a-zA-Z][a-zA-Z\d]*$", input) and len(input) <= 12:
        	return True
	else :
		return False
