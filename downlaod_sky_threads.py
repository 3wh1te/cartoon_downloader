#coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import threading

def mkdir(path):
    '''
    防止目录存在
    '''
    if not os.path.exists(path):
        os.mkdir(path)

def SavePic(filename, url):
    '''
    通过requests库
    将抓取到的图片保存到本地
    '''
    content = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(content)

def SaveChapter(num,path,url):
    '''
    下载一整章
    '''
    print("第%s章开始，一共%s页" % (path, num))
    for index in range(1,int(num) + 1):
        # 为防止brower共享问题，为每一个创建一个brower
        browser = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-windows\\bin\phantomjs.exe')
        browser.get('http://www.125084.com/' + url%(str(index)))
        browser.implicitly_wait(3)
        # 提取照片url
        pic_url = browser.find_element_by_id('iBody').find_element_by_tag_name("img").get_attribute('src')
        # 下载
        SavePic(path + '/' + str(index )+ '.jpg', pic_url)
    print("第%s章完成，一共%s页"%(path,num))


html = requests.get('http://www.125084.com/manhua13418.html')
bs = BeautifulSoup(html.text, "html.parser")
# 提取每章漫画所在的位置，其实这个文件夹是有规律的，也可以直接生成
chapter_list = bs.find('ul',attrs={"class":'cVolUl'})
dirname = 10
threads = []
for chapter in list(chapter_list.children)[20:26]:
    pos = chapter.a['href']
    home_html = requests.get('http://www.125084.com/' + pos).text
    html_parser = BeautifulSoup(home_html,"html.parser")
    # 提取该章的页数
    page_num = html_parser.find('div',attrs={"class":'cH1'}).b.text.split('/')[1]
    # 创建该章的文件夹，也可以在线程里面创建
    mkdir(str(dirname))
    # 每一页漫画的位置%s为1 2 3 4 5……
    pos = pos.split('/')[1] + '/%s.html?s=4'
    # 创建线程
    thread = threading.Thread(target=SaveChapter,args=[page_num,str(dirname),pos])
    # 启动线程
    thread.start()
    dirname -= 1
    threads.append(thread)
# 阻塞主线程，等待所有线程结束再推出主线程
for t in threads:
    t.join()