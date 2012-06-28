#!/usr/bin/python
#-*- coding:utf8 -*-

import urllib2, time, re,pymongo, MySQLdb, base64

if __name__ == "__main__":
  baseUrl = urllib2.Request('http://blog.csdn.net/cnhzgb?viewmode=contents')
  baseUrl.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17')
  resp = urllib2.urlopen(baseUrl)
  page = resp.read()
  resp.close()

  conn = MySQLdb.connect('mysql.sql2.cdncenter.net', user='sq_huwai114', passwd='#####')
  conn.select_db('sq_huwai114')
  cursor = conn.cursor()

  linkPat = re.compile(r"<span class=\"link_title\"><a href=\"(.+?)\">(.+?)</a>", re.S | re.I | re.M)
  for mat in linkPat.finditer(page):  
    link = 'http://blog.csdn.net' + mat.group(1)
    title = mat.group(2).strip()
    print "~~~~~~~~~~ " , link , title
    num = cursor.execute("select * from csdn where link = '%s'" % (link))
    exist = num >= 1

    req = urllib2.Request(link)
    req.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17')
    resp = urllib2.urlopen(req)
    page = resp.read()
    resp.close()

    ## print  "\n\n\n " + page + "\n\n\n\n\n"

    pat = re.compile(r"(<div id=\"article_content\".+?)<div class=\"share_buttons\"", re.S | re.I | re.M)
    has = False
    for m in pat.finditer(page):
      content = m.group(1)
      print content
      has = True

    if has == False:
        print "!!!!!!!!!!!!!!! content not find"
        break

    print "\n\n\n"

    content = base64.encodestring(content)
    title = base64.encodestring(title)
    if exist:
      print "update"
      cursor.execute("update csdn set title='%s',content='%s' where link = '%s'" % (title, content, link))
    else:
      print "insert"
      cursor.execute("insert into csdn (link, title, content) values ('%s', '%s', '%s')" % (link, title, content))
    conn.commit()

    time.sleep(3)
    



