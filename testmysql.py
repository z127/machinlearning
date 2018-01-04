#!/usr/bin python
# -*- coding: utf-8 -*-
import pymysql
connection=pymysql.connect(host='10.141.212.110',
                           user='root',
                           password='root',
                           db='monitor',
                           port=3306,
                           charset='utf8')
try:
    #获取一个游标
   with connection.cursor() as cursor:
       sql='select * from cpu_usagetest'
       cout=cursor.execute(sql)
       print("number： "+str(cout))

       for row in cursor.fetchall():
          # print('%s\t%s\t%s' %row)

            #注意int类型需要使用str函数转义
           print('  ip： '+str(row[0])+"  cpu_used： "+str(row[1]) )
       connection.commit()

finally:
    connection.close()