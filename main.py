import urllib.request
from lxml import etree
import csv
import re

# 获取页面 这里的页面是检索出来的符合条件的所有房屋简略信息的页面
def get_page(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    #print(html)
    return html

#获取总页数
def get_page_num(url):
    html = get_page(url)
    pagenum = re.findall(r'"totalPage":(.+?),"curPage"',html)[0]
    #re.findall（返回string中所有与pattern相匹配的全部字符串，返回形式为数组）
    pagenum = int(pagenum)
    return pagenum

# 获取当前页面中所有简略信息房子的url（包括后面的页数）
def get_house_url_current_page(url):
    print("数据读取中...")
    list_house_url_current_page = []
    pagenum = get_page_num(url)
    if pagenum == 1:
        print('正在读取第1页url信息...')
        html = get_page(url)
        selector = etree.HTML(html)
        house_url_list_li = selector.xpath('/html/body/div[5]/div[1]/ul/li')
        for li in house_url_list_li:
            house_url = li.xpath('div/div[1]/a/@href')[0]
            list_house_url_current_page.append(house_url)
    else:
        for i in range(1,pagenum+1):
        #for i in range(1, 11):
            print('正在读取第'+str(i)+'页url信息...')
            url1 = url + 'pg' + str(i)
            html = get_page(url1)
            selector = etree.HTML(html)
            house_url_list_li = selector.xpath('/html/body/div[5]/div[1]/ul/li')
            for li in house_url_list_li:
                house_url = li.xpath('div/div[1]/a/@href')[0]
                list_house_url_current_page.append(house_url)
    print('url读取完成')
    return list_house_url_current_page   #这里已经获取了当前页的所有房屋信息的链接

#获取页面详细数据
def get_data(url,i):
    print('正在读取第'+str(i)+'个房源信息')
    list_data = []
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    selector = etree.HTML(html)

    #房源链接
    list_data.append(url)

    #房源信息
    Information = selector.xpath('/html/body/div[4]/div/text()')[0]
    Information1 = Information.split()
    for i in Information1:
        list_data.append(i)
    #房间价格
    Price = selector.xpath('/html/body/section[1]/div[2]/div[2]/div[1]/span/i/text()')[0] + '万'
    list_data.append(Price)
    return list_data

def write_data(data):
    print('数据写入中...')
    with open('建设路.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['链接','地址', '户型','面积','价格'])
        writer.writerows(data)
        print('数据写入成功')

def main():
    i = 1
    data = []
    for url in get_house_url_current_page('https://cd.lianjia.com/chengjiao/jianshelu/'):
        data.append(get_data(url,i))
        i = i+1
    print('房源信息读取完成')
    write_data(data)

main()
