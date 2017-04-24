'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Built in functions'''
def index():
    import datetime
    import MySQLdb
    y=str(datetime.datetime.now().year)
    sql='select * from %s where datetime = (select max(datetime) from %s);'%(dbselect(y),dbselect(y))
    db=MySQLdb.connect("localhost","root","iiits@123","weather")
    cursor=db.cursor()
    cursor.execute(sql)
    a=cursor.fetchall()
    x=a[0]
    dattime=str(x[0])   
    dat=dattime.split()[0]
    k=dat.split('-')
    dat=k[2]+"-"+k[1]+"-"+k[0]
    tim=dattime.split()[1]
    stemp=str(x[1])
    swind=str(x[3])
    spress=str(x[4])
    shumid=str(x[2])
    srain=str(x[5])
    return locals()
    

def error():
    s=''
    link=''
    if request.args[0]=='1':
        s='date'
        l=URL('day')
    elif request.args[0]=='2':
        s='month'
        l=URL('month')
    elif request.args[0]=='3':
        s='year'
        l=URL('year')
    else:
        return "Error: This page is not available"
    return locals()

def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()

def test():
    import MySQLdb
    a='2014-03-09'
    b=1
    s=datakey(int(b))
    sql="select avg(%s) from weath14 where date(datetime)='%s' group by hour(datetime);"%(s,str(a))
    db=MySQLdb.connect("localhost","root","deepdeepu27","weather")
    cursor=db.cursor()
    cursor.execute(sql)
    a=cursor.fetchall()
    i=0
    meandata=[]
    for x in a:
        m=str(x[0])
        meandata.append([i,float(m)])
        i=i+1
    return locals()
'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Selectors for pre formatting'''

def monthkey(a):
    if a==1:
        return 'January'
    elif a==2:
        return 'February'
    elif a==3:
        return 'March'
    elif a==4:
        return 'April'
    elif a==5:
        return 'May'
    elif a==6:
        return 'June'
    elif a==7:
        return 'July'
    elif a==8:
        return 'August'
    elif a==9:
        return 'September'
    elif a==10:
        return 'October'
    elif a==11:
        return 'November'
    elif a==12:
        return 'December'

def yearkey(n):
    if n==1:
        return 2014
    elif n==2:
        return 2015

def yearkey2(n):
    if n==1:
        return 2013
    elif n==2:
        return 2014
    elif n==3:
        return 2015

def dbselect(a):
    if a=='2014' or a=='2013':
        return 'weath14'
    elif a=='2015':
        return 'weath15'
    elif a=='2016':
        return 'weath15'

def datakey(n):
    if n==1:
        return "temp"
    elif n==2:
        return "press"
    elif n==3:
        return "wind"
    elif n==4:
        return "humid"
    elif n==5:
        return "rain"

def label(n):
    if n==1:
        return "Temperature"
    elif n==2:
        return "Pressure"
    elif n==3:
        return "Wind"
    elif n==4:
        return "Humidity"
    elif n==5:
        return "Rain"

def labeldata(n):
    if n==1:
        return "Mean"
    elif n==2:
        return "Maximum"
    elif n==3:
        return "Minimum"
    elif n==4:
        return "Standard Deviation"
    elif n==5:
        return "Median"

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Database selector'''

def select(sql):
    import MySQLdb
    db=MySQLdb.connect("localhost","root","iiits@123","weather")
    cursor=db.cursor()
    cursor.execute(sql)
    a=cursor.fetchall()
    i=0
    meandata=[]
    for x in a:
        m=str(x[0])
        meandata.append([i,float(m)])
        i=i+1
    return meandata

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

def history():
    
    formd=SQLFORM.factory(Field("Date",'date'),Field('Data',requires=IS_EMPTY_OR(IS_IN_SET([(1,'Mean'), (2,'Max'), (3,'Min'), (4,'Standard Deviation'), (5,'Median')]))))
    formd.process(formname='formd')
    
    formm=SQLFORM.factory(Field("Month",requires=IS_IN_SET([(1,'January'), (2,'February'), (3,'March'), (4,'April'), (5,'May'),(6,'June'), (7,'July'), (8,'August'), (9,'September'), (10,'October'),(11,'November'),(12,'December')])),Field('Year',requires=IS_IN_SET([(1,'2014'), (2,'2015')])),Field('Data',requires=IS_IN_SET([(1,'Mean'), (2,'Maximum'), (3,'Minimum'), (4,'Standard Deviation'), (5,'Median')])))
    formm.process(formname='formm')

    formy=SQLFORM.factory(Field("Year",requires=IS_IN_SET([(1,'2013'), (2,'2014'), (3,'2015')])),Field('Data',requires=IS_IN_SET([(1,'Mean'), (2,'Maximum'), (3,'Minimum'), (4,'Standard Deviation'), (5,'Median')])))
    formy.process(formname='formy')

    if formd.accepted:
            redirect(URL('dayres',args=[formd.vars.Date,formd.vars.Data]))
    if formy.accepted:
            redirect(URL('yearres',args=[formy.vars.Data,yearkey2(int(formy.vars.Year))]))
    if formm.accepted:
            redirect(URL('monthres',args=[formm.vars.Month,formm.vars.Data,yearkey(int(formm.vars.Year))]))
    return locals()


'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Main for Day'''

def day():
    form=SQLFORM.factory(Field("Date",'date'),Field('Data',requires=IS_EMPTY_OR(IS_IN_SET([(1,'Mean'), (2,'Max'), (3,'Min'), (4,'Standard Deviation'), (5,'Median')])))).process()
    if form.accepted:
            redirect(URL('dayres',args=[form.vars.Date,form.vars.Data]))
    return locals()

def dayres():
    Date=request.args[0]
    d=Date.split("-")
    Date=d[2]+"-"+d[1]+"-"+d[0]
    s=""
    if request.args[1]=='1':
        try:
            tempdata=str(meancalcday(request.args[0],1))
            pressdata=str(meancalcday(request.args[0],2))
            winddata=str(meancalcday(request.args[0],3))
            humiddata=str(meancalcday(request.args[0],4))
            raindata=str(meancalcday(request.args[0],5))
        except AttributeError:
            redirect(URL('error',args=[1]))
        if len(tempdata)<3:
            redirect(URL('error',args=[1]))
        s=labeldata(int(request.args[1]))
    elif request.args[1]=='2':
        try:
            tempdata=str(maxcalcday(request.args[0],1))
            pressdata=str(maxcalcday(request.args[0],2))
            winddata=str(maxcalcday(request.args[0],3))
            humiddata=str(maxcalcday(request.args[0],4))
            raindata=str(maxcalcday(request.args[0],5))
        except AttributeError:
            redirect(URL('error',args=[1]))
        if len(tempdata)<3:
            redirect(URL('error',args=[1]))
        s=labeldata(int(request.args[1]))
    elif request.args[1]=='3':
        try:
            tempdata=str(mincalcday(request.args[0],1))
            pressdata=str(mincalcday(request.args[0],2))
            winddata=str(mincalcday(request.args[0],3))
            humiddata=str(mincalcday(request.args[0],4))
            raindata=str(mincalcday(request.args[0],5))
        except AttributeError:
            redirect(URL('error',args=[1]))
        if len(tempdata)<3:
            redirect(URL('error',args=[1]))
        s=labeldata(int(request.args[1]))
    elif request.args[1]=='4':
        try:
            tempdata=str(devcalcday(request.args[0],1))
            pressdata=str(devcalcday(request.args[0],2))
            winddata=str(devcalcday(request.args[0],3))
            humiddata=str(devcalcday(request.args[0],4))
            raindata=str(devcalcday(request.args[0],5))
        except AttributeError:
            redirect(URL('error',args=[1]))
        if len(tempdata)<3:
            redirect(URL('error',args=[1]))
        s=labeldata(int(request.args[1]))
    elif request.args[1]=='5':
        try:
            tempdata=str(medcalcday(request.args[0],1))
            pressdata=str(medcalcday(request.args[0],2))
            winddata=str(medcalcday(request.args[0],3))
            humiddata=str(medcalcday(request.args[0],4))
            raindata=str(medcalcday(request.args[0],5))
        except AttributeError:
            redirect(URL('error',args=[1]))
        if len(tempdata)<3:
            redirect(URL('error',args=[1]))
        s=labeldata(int(request.args[1]))
    else:
        return "Error 404"
    return locals()


'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Day Calculators'''

def meancalcday(a,b):
    s=datakey(int(b))
    k=dbselect(a[0:4])
    sql="select avg(%s) from %s where date(datetime)='%s' group by hour(datetime);"%(s,k,str(a))
    return select(sql)

def maxcalcday(a,b):
    k=dbselect(a[0:4])
    s=datakey(int(b))
    sql="select max(%s) from %s where date(datetime)='%s' group by hour(datetime);"%(s,k,str(a))
    return select(sql)

def mincalcday(a,b):
    s=datakey(int(b))
    k=dbselect(a[0:4])
    sql="select min(%s) from %s where date(datetime)='%s' group by hour(datetime);"%(s,k,str(a))
    return select(sql)

def medcalcday(a,b):
    s=datakey(int(b))
    k=dbselect(a[0:4])
    sql="select %s from %s where date(datetime)='%s' and minute(datetime)='30' group by hour(datetime);"%(s,k,str(a))
    return select(sql)

def devcalcday(a,b):
    k=dbselect(a[0:4])
    s=datakey(int(b))
    sql="select std(%s) from %s where date(datetime)='%s' group by hour(datetime);"%(s,k,str(a))
    return select(sql)

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Main for Month'''

def month():
    form=SQLFORM.factory(Field("Month",requires=IS_IN_SET([(1,'January'), (2,'February'), (3,'March'), (4,'April'), (5,'May'),(6,'June'), (7,'July'), (8,'August'), (9,'September'), (10,'October'),(11,'November'),(12,'December')])),Field('Year',requires=IS_IN_SET([(1,'2014'), (2,'2015')])),Field('Data',requires=IS_IN_SET([(1,'Mean'), (2,'Maximum'), (3,'Minimum'), (4,'Standard Deviation'), (5,'Median')]))).process()
    if form.accepted:
        redirect(URL('monthres',args=[form.vars.Month,form.vars.Data,yearkey(int(form.vars.Year))]))
    return locals()


def monthres():
    s=labeldata(int(request.args[1]))
    month=monthkey(int(request.args[0]))
    year=request.args[2]
    if request.args[1]=='1':    
        try:
            tempdata=meanmonth(1,request.args[0],request.args[2])
            pressdata=meanmonth(2,request.args[0],request.args[2])
            winddata=meanmonth(3,request.args[0],request.args[2])
            humiddata=meanmonth(4,request.args[0],request.args[2])
            raindata=meanmonth(5,request.args[0],request.args[2])
        except AttributeError:
            redirect(URL('error',args=['2']))
        if len(tempdata)<3:
            redirect(URL('error',args=[2]))
    elif request.args[1]=='2':    
        try:
            tempdata=maxmonth(1,request.args[0],request.args[2])
            pressdata=maxmonth(2,request.args[0],request.args[2])
            winddata=maxmonth(3,request.args[0],request.args[2])
            humiddata=maxmonth(4,request.args[0],request.args[2])
            raindata=maxmonth(5,request.args[0],request.args[2])
        except AttributeError:
            redirect(URL('error',args=['2']))
        if len(tempdata)<3:
            redirect(URL('error',args=[2]))
    elif request.args[1]=='3':    
        try:
            tempdata=minmonth(1,request.args[0],request.args[2])
            pressdata=minmonth(2,request.args[0],request.args[2])
            winddata=minmonth(3,request.args[0],request.args[2])
            humiddata=minmonth(4,request.args[0],request.args[2])
            raindata=minmonth(5,request.args[0],request.args[2])
        except AttributeError:
            redirect(URL('error',args=['2']))
        if len(tempdata)<3:
            redirect(URL('error',args=[2]))
    elif request.args[1]=='4':    
        try:
            tempdata=devmonth(1,request.args[0],request.args[2])
            pressdata=devmonth(2,request.args[0],request.args[2])
            winddata=devmonth(3,request.args[0],request.args[2])
            humiddata=devmonth(4,request.args[0],request.args[2])
            raindata=devmonth(5,request.args[0],request.args[2])
        except AttributeError:
            redirect(URL('error',args=['2']))
        if len(tempdata)<3:
            redirect(URL('error',args=[2]))
    elif request.args[1]=='5':    
        try:
            tempdata=medmonth(1,request.args[0],request.args[2])
            pressdata=medmonth(2,request.args[0],request.args[2])
            winddata=medmonth(3,request.args[0],request.args[2])
            humiddata=medmonth(4,request.args[0],request.args[2])
            raindata=medmonth(5,request.args[0],request.args[2])
        except AttributeError:
            redirect(URL('error',args=['2']))
        if len(tempdata)<3:
            redirect(URL('error',args=[2]))
    return locals()

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Calculators for Month'''

def meanmonth(a,b,c):
    s=datakey(int(a))
    k=dbselect(c)
    sql="select avg(%s) from %s where month(datetime)='%s' and year(datetime)='%s' group by date(datetime);"%(s,k,str(b),c)
    return select(sql)

def maxmonth(a,b,c):
    s=datakey(int(a))
    k=dbselect(c)
    sql="select max(%s) from %s where month(datetime)='%s' and year(datetime)='%s' group by date(datetime);"%(s,k,str(b),c)
    return select(sql)

def minmonth(a,b,c):
    s=datakey(int(a))
    k=dbselect(c)
    sql="select min(%s) from %s where month(datetime)='%s' and year(datetime)='%s' group by date(datetime);"%(s,k,str(b),c)
    return select(sql)

def medmonth(a,b,c):
    s=datakey(int(a))
    k=dbselect(c)
    sql="select %s from %s where month(datetime)='%s' and year(datetime)='%s' and hour(datetime)='12' group by date(datetime);"%(s,k,str(b),c)
    return select(sql)

def devmonth(a,b,c):
    s=datakey(int(a))
    k=dbselect(c)
    sql="select std(%s) from %s where month(datetime)='%s' and year(datetime)='%s' group by date(datetime);"%(s,k,str(b),c)
    return select(sql)

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Main for Year'''

def year():
    formy=SQLFORM.factory(Field("Year",requires=IS_IN_SET([(1,'2013'), (2,'2014'), (3,'2015')])),Field('Data',requires=IS_IN_SET([(1,'Mean'), (2,'Maximum'), (3,'Minimum'), (4,'Standard Deviation'), (5,'Median')])))
    formy.process(formname='formy')
    if formy.accepted:
            redirect(URL('yearres',args=[formy.vars.Data,yearkey2(int(formy.vars.Year))]))
    return locals()


def yearres():
    from operator import itemgetter
    year=request.args[1]
    s=labeldata(int(request.args[0]))
    if request.args[0]=='1':
        try:
            tempdata=meanyear(1,request.args[1])
            pressdata=meanyear(2,request.args[1])
            winddata=meanyear(3,request.args[1])
            humiddata=meanyear(4,request.args[1])
            raindata=meanyear(5,request.args[1])
        except AttributeError:
            redirect(URL('error',args=[3]))
        if len(tempdata)<3:
            redirect(URL('error',args=[3]))
    elif request.args[0]=='2':
        try:
            tempdata=maxyear(1,request.args[1])
            pressdata=maxyear(2,request.args[1])
            winddata=maxyear(3,request.args[1])
            humiddata=maxyear(4,request.args[1])
            raindata=maxyear(5,request.args[1])
        except AttributeError:
            redirect(URL('error',args=[3]))
        if len(tempdata)<3:
            redirect(URL('error',args=[3]))
    elif request.args[0]=='3':
        try:
            tempdata=minyear(1,request.args[1])
            pressdata=minyear(2,request.args[1])
            winddata=minyear(3,request.args[1])
            humiddata=minyear(4,request.args[1])
            raindata=minyear(5,request.args[1])
        except AttributeError:
            redirect(URL('error',args=[3]))
        if len(tempdata)<3:
            redirect(URL('error',args=[3]))
    elif request.args[0]=='4':
        try:
            tempdata=devyear(1,request.args[1])
            pressdata=devyear(2,request.args[1])
            winddata=devyear(3,request.args[1])
            humiddata=devyear(4,request.args[1])
            raindata=devyear(5,request.args[1])
        except AttributeError:
            redirect(URL('error',args=[3]))
        if len(tempdata)<3:
            redirect(URL('error',args=[3]))
    elif request.args[0]=='5':
        try:
            tempdata=medyear(1,request.args[1])
            pressdata=medyear(2,request.args[1])
            winddata=medyear(3,request.args[1])
            humiddata=medyear(4,request.args[1])
            raindata=medyear(5,request.args[1])
        except AttributeError:
            redirect(URL('error',args=[3]))
        if len(tempdata)<3:
            redirect(URL('error',args=[3]))
    return locals()

'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

'''Calculators for Year'''

def meanyear(a,b):
    s=datakey(int(a))
    k=dbselect(b)
    sql="select avg(%s) from %s where year(datetime)='%s' group by date(datetime);"%(s,k,b)
    return select(sql)

def maxyear(a,b):
    s=datakey(int(a))
    k=dbselect(b)
    sql="select max(%s) from %s where year(datetime)='%s' group by date(datetime);"%(s,k,b)
    return select(sql)

def minyear(a,b):
    s=datakey(int(a))
    k=dbselect(b)
    sql="select min(%s) from %s where year(datetime)='%s' group by date(datetime);"%(s,k,b)
    return select(sql)

def medyear(a,b):
    s=datakey(int(a))
    k=dbselect(b)
    sql="select %s from %s where hour(datetime)='12' and year(datetime)='%s'group by date(datetime);"%(s,k,b)
    return select(sql)

def devyear(a,b):
    s=datakey(int(a))
    k=dbselect(b)
    sql="select std(%s) from %s where year(datetime)='%s'group by date(datetime);"%(s,k,b)
    return select(sql)
'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
