#!/usr/bin/python
# coding:utf-8
# Author: zhoulin
# Date:20161112

from bs4 import BeautifulSoup
import urllib2
import re
import time
import sys
import os
import zlib
import commands

reload(sys)                      # reload 才能调用 setdefaultencoding 方法
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'

def control_link(link):
    link = str(link)
    if link[0:2] == '//':
        link = "http:" + link
    elif link.startswith('.'):
        link = root_url + link[1:]
    elif link.startswith('/'):
        link = root_url + link
    return link

def download_img(download_list,path):
    for img_url in download_list:
        try:
            request = urllib2.Request(img_url)
            request.add_header('Accept-Encoding','gzip, deflate, sdch')
            request.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6,bs;q=0.4,zh-TW;q=0.2')
            request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
            request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            request.add_header('Referer','http://rb.arzon.jp/item_1340270.html')
            request.add_header('Cookie','PHPSESSID=fdld9oe628f0k0qiuibvleaq65')
            request.add_header('Host','rb.arzon.jp')
            f_img = open(os.path.join(path, img_url.split('/')[-1]),'wb')
            f_img.write(urllib2.urlopen(request).read())
            f_img.close()
        except Exception as e:
            print("Save file error:",img_url)
        # filename = img_url.split('/')[-1]
        # cmd = "curl '"+img_url+"' -H 'Upgrade-Insecure-Requests: 1' -H 'Cookie: PHPSESSID=fdld9oe628f0k0qiuibvleaq65' -H 'Referer: http://rb.arzon.jp/item_961706.html' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' --compressed -o "+os.path.join(path,filename)
        # status,output = commands.getstatusoutput(cmd)
        # if not status == 0:
        #     print("Download :",img_url," error,error msg is:",output)

def download_html(url):
    request = urllib2.Request(url)
    request.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,bs;q=0.4,zh-TW;q=0.2')
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request.add_header('Referer', 'http://rb.arzon.jp/item_1340270.html')
    request.add_header('Cookie', 'PHPSESSID=fdld9oe628f0k0qiuibvleaq65')
    request.add_header('Host', 'rb.arzon.jp')
    response = urllib2.urlopen(request)
    if response.code == 200:
        content = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        return content
    else:
        print "Response code is ",response.code,",,url is ",url

def SpiderMain(root_url,path):
    search_con = download_html(root_url)
    search_soup = BeautifulSoup(search_con, "html.parser")
    item_con = search_soup.find('li',class_="topContents")
    item_url = item_con.find(href=re.compile(r'/item_[0-9]*.html')).attrs['href']

    # spider items
    if item_url is None:
        print "Error,not found item in ",root_url
    else:
        item_con = download_html(control_link(item_url))
        item_soup = BeautifulSoup(item_con, "html.parser")
        download_list = []
        ## spider fengmian
        fengmian_con = item_soup.find(id="productExtra")
        img = fengmian_con.find('a')
        download_list.append(control_link(img.attrs['href']))

        ##spider info
        identifer_soup = item_soup.find(id="productIdentifier")
        with open(os.path.join(path,'info.txt'),'w') as f:
            f.write(identifer_soup.get_text())

        ##sipder screenshot
        screnshot_soup = item_soup.find(id="sample-image-block")
        if screnshot_soup is not None:
            for img in screnshot_soup.find_all('a'):
                download_list.append(control_link(img.attrs['href']))

            download_img(download_list,path)
        else:
            print "no screenshot for item:",item_url
        # print item_con.find(href='/item_1340698.html')



if __name__ == '__main__':
    root_dir = os.getcwd()
    # root_url = "http://rb.arzon.jp"
    root_url = "https://avmo.pw/cn/search/"
    search_para = 'itemlist_b.html?&q=VENU-'
    for i in xrange(001,661):
        i = "%03d"%i
        try:
            path = os.path.join(root_dir,"VENU-"+str(i))
            if not os.path.exists(path):
                os.mkdir(path)
            SpiderMain(root_url+"/"+search_para+str(i),path)
            print "Success ----VENU-",i
            time.sleep(1)
        except Exception as e:
            print "Error----VENU-",i,"   error code is:",e