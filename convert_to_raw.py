#!/usr/bin/python

file = "a041 8007 8f36 0002 006e 0f33 0fff 0061 0f35 0002 0070 0fd4 003c 0006 0040 0079 009c 0f4f 000d 006d 0fdc 0009 000a 0040 0072 0063 0fdb 0009 000b 003f 00d0 4013 e000 c001"

file = file.split()
for i in file:
    i=int(i,16)
    i = i & 0x0fff
    if i & 0x0800:
        i -= 4096
    print i,

