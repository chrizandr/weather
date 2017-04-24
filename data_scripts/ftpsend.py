import os
print "Importing OS library..."
currentdir=os.getcwd()
print "Current location found to be " + currentdir

print "Checking all files in current directory..."
insys=os.listdir(currentdir)
print str(len(insys)) + " Files found "
from ftplib import FTP
print "Connecting to FTP server..."
ftp=FTP('ftp.byethost24.com')
print "Attempting login..."
ftp.login('b24_17771518','iiits@123')
ftp.cwd('htdocs')

inftp=ftp.nlst()
print str(len(inftp))+" Files found in FTP server,"

print "Starting downlaod of new files..."
for filename in inftp:
        if filename not in insys and filename !='.' and filename!='..':
                try:
                        ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
                except:
                        print "There was some Error uploading the file " + filename + ", Please try again"
print "Files successfully downloaded from the server"

