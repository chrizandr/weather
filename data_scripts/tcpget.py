import socket
import sys
s = socket.socket()
s.bind(('',34567))
print "Waiting to receive files"
while 1:
        s.listen(10)
        sc, address = s.accept()
        print "Connection established with " + str(address[0]) + " on port: " + str(address[1])
        k=sc.recv(1024)
        k=k.strip()
        sc.send("Server: Ready to receive " + k)
        print "Receiving "  + k
        f=open(k,'wb')
        l = sc.recv(1024)
        while (l):
                f.write(l)
                l = sc.recv(1024)
        f.close()
        print k + "received"
        sc.close()
        print "Closing connection"
