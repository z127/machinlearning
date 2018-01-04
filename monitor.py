#!/usr/bin/python
# author:killvoon
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pymysql
import datetime
##定义主机列表(先只弄linux)
linux = ['10.141.212.110']


def connectHost(ip, uname='root', passwd='Fdwangp123'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=uname, password=passwd)
    return ssh


def MainCheck():
#查看linux文件系统使用率
   #建立主机连接
 for a in range(len(linux)):
   try:
    ssh=connectHost(linux[a])
    #查看文件系统命令
    cmd="df -h|sed '1d'|awk '{print $2\",\" $3\",\" $4\",\" $6\",\" $5}'"
    stdin,stdout,stderr=ssh.exec_command(cmd)
    filesystem_usage=stdout.readlines()
    #查看系统时间
    chk="date \"+%Y-%m-%d %H:%M:%S\""
    stdin,stdout,stderr=ssh.exec_command(chk)
    check_time=stdout.readlines()
    check_time=check_time[0]
    #查看主机名
    hostname="hostname"
    stdin,stdout,stderr=ssh.exec_command(hostname)
    hostname=stdout.readlines()
    hostname=hostname[0]
    #循环列表，将文件系统使用率插入到数据库中
    for i in range(len(filesystem_usage)):
      list_1=filesystem_usage[i]
      list_1=list(list_1.split(','))
      #print(len(list_1))
      sql='insert into filesys_usage values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' %(linux[a],hostname,list_1[0],list_1[1],list_1[2],list_1[3],list_1[4],check_time,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      #print(sql)
      db=connectDB()
      sqlDML(sql,db)

    #查看cpu使用率，并将信息写入到数据库中(取三次平均值)
    cpu="vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
    stdin,stdout,stderr=ssh.exec_command(cpu)
    cpu=stdout.readlines()
    cpu_usage=str(round((100 - (int(cpu[0])+int(cpu[1])+int(cpu[2]))/3),2))+'%'
    sql="insert into cpu_usage values('%s','%s','%s','%s')" %(linux[a],cpu_usage,check_time,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db=connectDB()
    sqlDML(sql,db)

    #查看内存使用率，并将信息写入到数据库中

    mem="cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
    stdin,stdout,stderr=ssh.exec_command(mem)
    mem=stdout.readlines()
    mem_total=round(int(mem[0])/1024)
    mem_total_free=round(int(mem[1])/1024) + round(int(mem[2])/1024) +round(int(mem[3])/1024)
    mem_usage=str(round(((mem_total-round(int(mem[1])/1024))/mem_total)*100,2))+"%"
    sql="insert into mem_usage values('%s','%s','%s','%s','%s','%s','%s','%s')" %(linux[a],str(round(int(mem[0])/1024))+"M",str(round(int(mem[1])/1024))+"M",str(round(int(mem[2])/1024))+"M",str(round(int(mem[3])/1024))+"M",mem_usage,check_time,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db=connectDB()
    sqlDML(sql,db)


   except TimeoutError:
       error='can not connect,please check server machine!'
       sql='insert into error_report values(\'%s\',\'%s\',\'%s\',)' %(linux[a],check_time,error)
       print("连接服务器 %s 异常" %(linux[a]))
       db=connectDB()
       sqlDML(sql,db)
       sendMail()
       continue


def connectDB(dbname='orcl'):
    connection=pymysql.connect(host='10.141.212.110',
                    user='root',
                    password='root',
                    db='monitor',
                    port=3306,
                    charset='utf8')
    return  connection

def sqlDML(sql, db):
    cr = db.cursor()
    cr.execute(sql)
    cr.close()
    db.commit()


##定义邮件函数

def sendMail():
    sender = 'xxxxxx@163.com'
    receiver = ['xxxx@qq.com', 'xxxx@qq.com']
    subject = "有监控报警邮件，请注意查收！"
    smtpserver = 'smtp.163.com'
    username = 'xxxxxxx@163.com'
    password = 'xxxxxxxxxxxx'
    msg = MIMEText('服务器连接出现问题！', 'plain', 'utf-8')  ##plain 换成text后便发送不了邮件正文
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    MainCheck()



