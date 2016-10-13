#
# by Taka Wang
#

from proximity import *

scanner = Scanner(loops=3)
while True:
    print 'start scanning'
    for beacon in scanner.scan():
        print beacon
