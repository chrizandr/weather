import socket
import os
print "Importing OS library..."
currentdir=os.getcwd()
print "Current location found to be " + currentdir

print "Checking all files in current directory..."
insys=os.listdir(currentdir)
print str(len(insys)) + " Files found "
exclude=['.','..','tcpsend.py','tcpget.py','format.py','ftpsend.py','ftpget.py','format']
for filename in insys:
        if filename not in exclude:
                s = socket.socket()
                host = socket.gethostname()
                port = 34567
                print "Connecting..."
                s.connect(("10.0.3.44", port))
                print "Attempting to send " + filename
                s.send(str(filename))
                l=s.recv(1024)
                print l
                print "Sending "+filename
                f=open(filename,'rb')
                l = f.read(1024)
                while (l):
                    s.send(l)
                    l = f.read(1024)
                print "File sent..."

