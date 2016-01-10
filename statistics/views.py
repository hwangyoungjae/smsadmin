# -*- encoding:utf8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import MySQLdb
DBHOST='192.168.20.131'
DBUSER='sms'
DBPASS='sms#@!'
DBNAME='sms'
DBPORT=3306
def dots(numeric):
    import locale
    locale.setlocale(locale.LC_ALL,'')
    return locale.format('%3f',numeric,1).rsplit('.',1)[0]

def main(req):
    class CLIENT:pass
    con=MySQLdb.connect(DBHOST,DBUSER,DBPASS,DBNAME,DBPORT)
    cur=con.cursor()
    cur.execute('SELECT no,client_user,INET_NTOA(allow_ip1),INET_NTOA(allow_ip2),INET_NTOA(allow_ip3),INET_NTOA(allow_ip4),INET_NTOA(allow_ip5),reg_date,status FROM sms_client ORDER BY no;')
    TMP_RESULT=cur.fetchall()
    clients=[]
    for row in TMP_RESULT:
        sms_clientNO,CLIENT_USER,ALLOW_IP1,ALLOW_IP2,ALLOW_IP3,ALLOW_IP4,ALLOW_IP5,REG_DATE,STATUS=row
        client=CLIENT()
        client.no=sms_clientNO
        client.name=CLIENT_USER
        client.allow=[]
        if ALLOW_IP1:client.allow.append(ALLOW_IP1)
        if ALLOW_IP2:client.allow.append(ALLOW_IP2)
        if ALLOW_IP3:client.allow.append(ALLOW_IP3)
        if ALLOW_IP4:client.allow.append(ALLOW_IP4)
        if ALLOW_IP5:client.allow.append(ALLOW_IP5)
        client.reg_date=REG_DATE.strftime('%Y/%m/%d')
        client.status=STATUS
        clients.append(client)
        
        cur.execute('SELECT SUM(sms_scnt),SUM(sms_fcnt),SUM(lms_scnt),SUM(lms_fcnt) FROM sms_statistics WHERE client_no=%s;',(sms_clientNO,))
        SS,SF,LS,LF=cur.fetchone()
        client.SS=dots(SS)
        client.SF=dots(SF)
        client.LS=dots(LS)
        client.LF=dots(LF)
    con.close()
    return render(req, 'statistics/main.html',{'clients':clients},)

def client_detail(req,NO,sdate=None,edate=None):
    class STATISTICS:
        def __init__(self,SDATE):
            self.SDATE=SDATE
        def __str__(self):
            return str(self.SDATE)
    statistics_list=[]
    con=MySQLdb.connect(DBHOST,DBUSER,DBPASS,DBNAME,DBPORT)
    cur=con.cursor()
    cur.execute('SELECT client_user FROM sms_client WHERE no=%s;',(NO,))
    client=cur.fetchone()[0]
    
    try:SDATE=req.GET['sdate']
    except KeyError:SDATE=None
    try:EDATE=req.GET['edate']
    except KeyError:EDATE=None
    try:
        PAGE=req.GET['page']
        PAGE=(int(PAGE)-1)*10
    except KeyError:PAGE=0
    
    if SDATE and not EDATE:
        cur.execute('SELECT COUNT(1) FROM sms_statistics WHERE client_no=%s AND TO_DAYS(sdate) >= TO_DAYS(%s);',(NO,SDATE,))
        COUNT=cur.fetchone()[0]
        cur.execute('SELECT sdate,sms_scnt,sms_fcnt,lms_scnt,lms_fcnt FROM sms_statistics WHERE client_no=%s AND TO_DAYS(sdate) >= TO_DAYS(%s) ORDER BY sdate DESC LIMIT %s,10;',(NO,SDATE,PAGE,))
    elif SDATE and EDATE:
        cur.execute('SELECT COUNT(1) FROM sms_statistics WHERE client_no=%s AND TO_DAYS(sdate) >= TO_DAYS(%s) AND TO_DAYS(sdate) <= TO_DAYS(%s);',(NO,SDATE,EDATE,))
        COUNT=cur.fetchone()[0]
        cur.execute('SELECT sdate,sms_scnt,sms_fcnt,lms_scnt,lms_fcnt FROM sms_statistics WHERE client_no=%s AND TO_DAYS(sdate) >= TO_DAYS(%s) AND TO_DAYS(sdate) <= TO_DAYS(%s) ORDER BY sdate DESC LIMIT %s,10;',(NO,SDATE,EDATE,PAGE,))
    else:
        cur.execute('SELECT COUNT(1) FROM sms_statistics WHERE client_no=%s;',(NO,))
        COUNT=cur.fetchone()[0]
        cur.execute('SELECT sdate,sms_scnt,sms_fcnt,lms_scnt,lms_fcnt FROM sms_statistics WHERE client_no=%s ORDER BY sdate DESC LIMIT %s,10 ;',(NO,PAGE,))
    for row in cur.fetchall():
        SDATE,SMS_SCNT,SMS_FCNT,LMS_SCNT,LMS_FCNT=row
        statistics=STATISTICS(SDATE)
        statistics.SS=dots(SMS_SCNT)
        statistics.SF=dots(SMS_FCNT)
        statistics.LS=dots(LMS_SCNT)
        statistics.LF=dots(LMS_FCNT)
        statistics_list.append(statistics)
    con.close()
    pages=range(1,(COUNT/10)+1)
    return render(req, 'statistics/client_detail.html',{'client':client,'statistics_list':statistics_list,'pages':pages})

























