# Import news from old website
# @todo class1: export from old
# @todo class1: import to django


import sys
from sys import stdout
import codecs


def die(msg):
    raise SystemExit(msg)
def error(msg):
    raise SystemExit('Error: '+msg)

def printf (fmt, *varargs):
    sys.stdout.write(fmt % varargs)


if (len(sys.argv) != 2):
    die ('Usage: %s <filename>' % sys.argv[0])

#f = open (sys.argv[1], 'r')
#for line in f:
#    print (line)

#for line in open (sys.argv[1], 'r'):
#    stdout.write(line)

for line in codecs.open (sys.argv[1], encoding='latin1'):
    stdout.write(line.encode('utf8'))

# or just read as str and then: line.decode('latin1') to get
# unicode object. django expects that when creating objects

#for line in codecs.open (sys.argv[1], encoding='latin1'):
#    stdout.write(repr(line))
