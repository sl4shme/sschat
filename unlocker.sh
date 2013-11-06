#!/usr/bin/python
import tools, time

count=0
while 1 :
        if not "OK" in open("lock"):
                count+=1
        else :
                count=0
        if count >= 5 :
                tools.releaseSpawnLock()
        time.sleep(5)




