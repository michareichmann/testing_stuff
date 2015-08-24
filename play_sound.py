#!/usr/bin/python

from time import sleep
import sys

try:
    import winsound
except ImportError:
    import os

    def playsound(frequency, duration):
        os.system('beep -f %s -l %s' % (frequency, duration))
else:
    def playsound(frequency, duration):
        winsound.Beep(frequency, duration)
try:
    duration = int(sys.argv[1])
except IndexError:
    duration = 300
a1 = pow(2, float(1) / 12)
p = 99
c, cis, d, dis, e, f, fis, g, gis, a, ais, b = range(12)
c3, cis3, d3, dis3, e3, f3, fis3, g3, gis3, a3, ais3, b3 = range(12, 24)
c2, cis2, d2, dis2, e2, f2, fis2, g2, gis2, a2, ais2, b2 = range(24, 36)
octave4 = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2]
octave = []

for i in octave4:
    octave.append(i)
for i in octave4:
    octave.append(i -12)
for i in octave4:
    octave.append(i - 24)



entchen = [c, d, e, f, g, g, a, a, a, a, g, p, a, a, a, a, g, p, f, f, f, f, e, e, g, g, g, g, c]
length1 = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2]
matters = [e2, f3, a3, dis, a3, f3, e2, f3, a3, dis, a3, f3, e2, f3, a3, dis, a3, f3, e2, f3, a3, dis, a3, b, b, a3, f3, b, dis, a3, f3]
length2 = [1,  1,  1,  1,   1,  1,  1,  1,  1,  1,   1,  1,  1,  1,  1,  1,   1,  1,  1,  1,  1,  1,   1,  1, 1,  1,  1, .5,1,   1,  1]


def tone(num):
    if num == 99:
        return 0
    return 440 * pow(a1, octave[num])


for i, j in zip(entchen, length1):
    if i == 99:
        sleep(0.3 * j)
    else:
        playsound(tone(i), duration * j)
