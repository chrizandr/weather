def date(a,b,c):
        da=''
        dm=''
        if a>=10:
                da=str(a);
        else:
                da='0'+str(a)
        if b>=10:
                dm=str(b);
        else:
                dm='0'+str(b)
        return da+'_'+dm+'_'+c+'.txt'

def makedate(d,t):
        dr=d.split('/')
        tr=t.split(':')
        hr=int(tr[0])
        mi=int(tr[1][0:-1])
        if tr[1][-1]=='p' and hr!=12:
                hr=hr+12
        if tr[1][-1]=='a' and hr==12:
                hr=0
        fhr=str(hr)
        fmin=str(mi)
        if hr<10:
                fhr='0'+fhr
        if mi<10:
                fmin='0'+fmin
        dy=int(dr[0])
        mn=int(dr[1])
        yr=int(dr[2])
        fdy=str(dy)
        fmn=str(mn)
        fyr=str(yr)
        if dy<10:
                fdy='0'+fdy
        if mn<10:
                fmn='0'+fmn
        if yr<10:
                fyr='0'+fyr
        return '20'+fyr+'-'+fmn+'-'+fdy+' '+fhr+':'+fmin+':00'


def getdb(m):
        if m=='2014':
                return 'weath14'
        elif m=='2015':
                return 'weath15'
def Todb(m):
        import MySQLdb
        db=MySQLdb.connect("localhost","root","iiits@123","weather")
        cursor=db.cursor()
        f=open(m+'.txt','r')
        for line in f:
                line=line.split(',')
                try:
                        sql="insert into %s values ('%s','%s','%s','%s','%s','%s')"%(getdb(m),line[0],line[1],line[2],line[3],line[4],line[5])
                        cursor.execute(sql)
                except MySQLdb.Error,e:
                        print e
        db.commit()
	db.close()
        return


def ToOneFile(m):
	f=open('.isdone','r')
	k=f.readline()
	k=k.split(',')
	f.close()        
	include=['0','1','2','3','4','5','6','7','8','9']
        name=m+'.txt'
        output=open(name,'w')
	print "Checking index file for previous entries"
	print "Collecting data from new files..."
        for i in range(1,32):
                for j in range(1,13):
                        s=date(i,j,m)
                        try:
				if s not in k:                                
					f=open(s,'r')				
					k.append(s)
		                        for l in f:
		                                line=l.split()
		                                if line[0][0] in include:
		                                        temp=makedate(str(line[0]),str(line[1]))
		                                        output.write(temp+',')
		                                        output.write(line[2]+',')
		                                        output.write(line[5]+',')
		                                        output.write(line[7]+',')
		                                        output.write(line[16]+',')
		                                        output.write(line[17])
		                                        output.write('\n')
					f.close()
				else:
					print s
                        except IOError:
                                continue
	print "All data formatted and written into "+name
        output.close();
	print "Index file .isdone updated."
	f=open('.isdone','w')
	for s in k:
		f.write(s)
		f.write(',')
	f.close()
        return m

k=raw_input("Enter year:")
ToOneFile(k)
Todb(k)

