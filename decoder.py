#!/usr/bin/python
__author__ = 'micha'

def get_addresses(levels):
    i = 0
    col = levels[0] * 12 + levels[1] * 2  + levels[4] % 2
    row = 80 - (levels[2] * 18 + levels[3] * 3 + levels[4] / 2)
    print col, row

while True:
    print 'Enter the five levels you want to decode with spaces (enter "1" to exit):'
    x = raw_input()
    if x == "1":
        print 'exiting decoder! bye'
        break
    levels = []
    for i in x.split():
        levels.append(int(i))
    get_addresses(levels)
