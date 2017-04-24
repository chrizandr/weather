import serial
import time
ser=serial.Serial(port='/dev/ttyS1',baudrate=2400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
while 1:
	s=raw_input(">>Enter file name: ")
	s.strip()
	print "Opening " + s +" ...."
	f=open(s,"r")
	print "File opened"
	#k=len(s)
	#k=20-k-6
	#for i in range(0,k)
	#	padd+=" "
	ser.write("##//--"+s+'\n')
	print "Sending the file..."
	time.sleep(1)
	for l in f:
		ser.write(l)
	print "File sent"
	print " "

