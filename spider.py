#!/usr/bin/python
# coding:utf-8
# Author: zhoulin
# Date:20161114
# Version:20161220
import urllib

from bs4 import BeautifulSoup
import urllib2
import re
import time
import sys
import os
import zlib
import commands
import socket
socket.setdefaulttimeout(15)

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
        print "downloading:"+img_url
        request = urllib2.Request(img_url)
        request.add_header('Accept-Encoding','gzip, deflate, sdch, br')
        request.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6,bs;q=0.4,zh-TW;q=0.2')
        request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Referer','https://avmo.pw/cn')
        request.add_header('Cookie','AD_enterTime=1479049398; AD_clic_j_POPUNDER=2; AD_juic_j_M_728x90=1; AD_javu_j_P_728x90=1; AD_exoc_j_POPUNDER=1; AD_juic_j_L_728x90=4; AD_adst_j_POPUNDER=2; _ga=GA1.2.1043844509.1479049395; AD_exoc_j_L_728x90=1')
        img_name = img_url.split('/')[-1]
        # with open(os.path.join(path, img_name),'wb') as f_img:
        #     f_img.write(urllib2.urlopen(request).read())

        # cmd = "curl '" + img_url + "' -H 'accept-encoding: gzip, deflate, sdch, br' -H 'accept-language: zh-CN,zh;q=0.8,en;q=0.6,bs;q=0.4,zh-TW;q=0.2' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'accept: image/webp,image/*,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: jp.netcdn.space' -H 'cookie: __cfduid=d22ad39ec3e2fbb4bc7dab64e61ff43e81479049454' -H 'referer: https://avmo.pw/cn/movie/2zj4' --compressed -o " + os.path.join(path, img_name)
        # status, output = commands.getstatusoutput(cmd)
        # if not status == 0:
        #     print("Download :", img_url, " error,error msg is:", output)

        try:
            urllib.urlretrieve(img_url, os.path.join(path, img_name))
        except Exception as e:
            print("Download :", img_url, " error,error msg is:", e)
            continue
        time.sleep(1)
        # filename = img_url.split('/')[-1]
        # cmd = "curl '"+img_url+"' -H 'Upgrade-Insecure-Requests: 1' -H 'Cookie: PHPSESSID=fdld9oe628f0k0qiuibvleaq65' -H 'Referer: http://rb.arzon.jp/item_961706.html' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' --compressed -o "+os.path.join(path,filename)
        # status,output = commands.getstatusoutput(cmd)
        # if not status == 0:
        #     print("Download :",img_url," error,error msg is:",output)

def download_html(url):
    request = urllib2.Request(url)
    request.add_header('Accept-Encoding', 'gzip, deflate, sdch, br')
    request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,bs;q=0.4,zh-TW;q=0.2')
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    request.add_header('Referer', 'https://avmo.pw/cn')
    request.add_header('Cookie',
                       'AD_enterTime=1479049398; AD_clic_j_POPUNDER=2; AD_juic_j_M_728x90=1; AD_javu_j_P_728x90=1; AD_exoc_j_POPUNDER=1; AD_juic_j_L_728x90=4; AD_adst_j_POPUNDER=2; _ga=GA1.2.1043844509.1479049395; AD_exoc_j_L_728x90=1')
    response = urllib2.urlopen(request)
    if response.code == 200:
        content = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        return content
    else:
        print "Response code is ",response.code,",url is ",url

def SpiderMain(root_url,itemRange):
    root_dir = os.getcwd()
    for i in itemRange:
        i = "%03d"%i

        item_search_url = root_url+serialName + "-"+i
        search_con = download_html(item_search_url)

        if not re.findall(serialName + "-"+i,search_con):
            print "[ERROR]:item " + serialName + "-" + i + " does not exist"
            continue

        search_soup = BeautifulSoup(search_con, "html.parser")
        page_con = search_soup.find_all('a',class_="movie-box")
        # print len(item_con)
        if len(page_con) == 1:
            item_url = page_con[0].attrs['href']
            # print item_url
        elif len(page_con) == 0:
            print "[ERROR]:item " + serialName + "-" +i+" does not exist"
            continue
        else:
            print "Search "+serialName + "-"+i+" have multi-result"
            for item in page_con:
                if re.findall(serialName + "-"+i,item.get_text()):
                    item_url = item.attrs['href']
                    break;
                else:
                    continue


        path = os.path.join(root_dir, serialName + "-" + i)
        if not os.path.exists(path):
            os.mkdir(path)

        # spider items
        item_con = download_html(control_link(item_url))
        item_soup = BeautifulSoup(item_con, "html.parser")
        download_list = []

        ## spider fengmian
        fengmian_con = item_soup.find('a',class_="bigImage")
        fengmian_url = fengmian_con.attrs['href']
        download_list.append(control_link(fengmian_url))

        ##spider info
        identifer_soup = item_soup.find('div',class_="col-md-3 info")
        info = identifer_soup.get_text()
        avatar_link = item_soup.find_all('a',class_="avatar-box")
        if len(avatar_link) == 1:
            info = info + u"演员作品列表:\n" +avatar_link[0].attrs['href']
        with open(os.path.join(path,'info.txt'),'w') as f:
            f.write(info)

        ##sipder screenshot
        screnshot_soup = item_soup.find(id="sample-waterfall")
        if screnshot_soup is not None:
            for img in screnshot_soup.find_all('a'):
                download_list.append(control_link(img.attrs['href']))
        else:
            print "no screenshot for " + serialName + "-"+i+" which url is ",item_url
        # print item_con.find(href='/item_1340698.html')
        # print download_list
        if download_list:
            download_img(download_list, path)
        time.sleep(2)



if __name__ == '__main__':
    global serialName
    serialName= "LXVS"
    root_url = "https://avmo.pw/cn/search/"
    itemRange = xrange(1,14)
    SpiderMain(root_url,itemRange)
