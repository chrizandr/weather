import socket
import os
print "Importing OS library..."
currentdir=os.getcwd()
print "Current location found to be " + currentdir

print "Checking all files in current directory..."
insys=os.listdir(currentdir)
print str(len(insys)) + " Files found "
exclude=['.','..','tcpsend.py','tcpget.py','format.py','ftpsend.py','ftpget.py','format','sshsend.py']
for filename in insys:
        if filename not in exclude:
                print "Attempting to send " + filename
                query="scp "+currentdir+"/"+filename+" iiit@10.0.1.89:/home/iiit/weather/weatherdata/" 
		#print query
                print "Sending "+filename              
		os.system(query)                
		print "File sent..."

