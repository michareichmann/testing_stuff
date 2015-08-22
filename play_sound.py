#!/usr/bin/python

from time import sleep
import sys
import math
try:
    import winsound
except ImportError:
    import os
    def playsound(frequency,duration):
        os.system('beep -f %s -l %s' % (frequency,duration))
else:
    def playsound(frequency,duration):
        winsound.Beep(frequency,duration)

a1 = pow(2, float(1)/12)
c,d,e,f,g,a,h,p = 0,1,2,3,4,5,6,99
octave = [-9, -7, -5, -4, -2, 0, 2, 3]
entchen = [c,d,e,f,g,g,a,a,a,a,g,p,a,a,a,a,g,p,f,f,f,f,e,e,g,g,g,g,c]
length =  [1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2]
def tone(num):
	if num == 99:
		return 0
	return 440 * pow(a1,octave[num])

for i,j in zip(entchen, length):
	if i == 99:
		sleep(0.3*j)
	else:
		playsound(tone(i), 300*j)

