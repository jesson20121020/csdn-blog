#!/usr/bin/python
#-*- coding:utf-8 -*-

import MySQLdb, base64, time


if __name__ == "__main__":
  conn = MySQLdb.connect('mysql.sql2.cdncenter.net', user='sq_huwai114', passwd='######')
  conn.select_db('sq_huwai114')
  cursor = conn.cursor()

  datas = cursor.execute("select * from csdn limit 0,5")
  for data in cursor.fetchall():
    title = base64.decodestring(data[1])
    content = base64.decodestring(data[2])
    print "title:%s\n%s\n\n\n\n\n" % (title, content)
    time.sleep(3)
  conn.close()
