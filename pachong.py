import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
from urllib.parse import quote

# 定义请求头
HEADERS = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

# 新建写入景点的csv文件，文件编码格式和写方式
csvfile = open('去哪儿景点.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csvfile)
# 写入第一行表头
writer.writerow(['区域', '名称', '景点id', '类型', '级别', '热度', '地址', '特色', '经纬度'])


# 定义一个下载景点内容的函数
def download_page(url):
    try:
        # 请求页面，获取景点信息
        data = requests.get(url, headers=HEADERS, allow_redirects=True).content
        return data
    except:
        pass


# 更新下载函数，如果状态码不为200时，就等待2秒后在下载
def download_soup_waitting(url):
    try:
        response = requests.get(url, headers=HEADERS, allow_redirects=False, timeout=5)
        if response.status_code == 200:
            html = response.content
            html = html.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            # 没有返回200，等待2秒后下载
            sleep(2)
            print('等待下载中')
            return download_soup_waitting(url)
    except:
        return ''


def getType(type, url):
    # 下载热点旅游数据为soup对象
    soup = download_soup_waitting(url)
    # 旅游景点对应的列表元素
    search_list = soup.find('div', attrs={'id': 'search-list'})
    # 找到所有的旅游景点项目， 并且对其进行遍历
    sight_items = search_list.findAll('div', attrs={'class': 'sight_item'})
    for sight_item in sight_items:
        name = sight_item['data-sight-name']
        districts = sight_item['data-districts']
        point = sight_item['data-point']
        address = sight_item['data-address']
        data_id = sight_item['data-id']
        level = sight_item.find('span', attrs={'class': 'level'})
        if level:
            level = level.text
        else:
            level = ''
        product_star_level = sight_item.find('span', attrs={'class': 'product_star_level'})
        if product_star_level:
            product_star_level = product_star_level.text
        else:
            product_star_level = ''
        intro = sight_item.find('div', attrs={'class': 'intro'})
        if intro:
            intro = intro['title']
        else:
            intro = ''
        writer.writerow(
            [districts.replace('\n', ''), name.replace('\n', ''), data_id.replace('\n', ''), type.replace('\n', ''),
             level.replace('\n', ''), product_star_level.replace('\n', ''), address.replace('\n', ''),
             intro.replace('\n', ''), point.replace('\n', '')]
        )
    # 找到向下翻页的按钮，如果发现，往下翻页，继续下载景区内容
    next = soup.find('a', attrs={'class': 'next'})
    if next:
        next_url = 'https://piao.qunar.com' + next['href']
        print(next_url)
        getType(type, next_url)


def getTypes():
    # 定义热门景点的类型
    types = ['自然风光', '文化古迹', '公园', '农家度假', '游乐场', '展馆', '城市观光', '运动健身']
    for type in types:
        # 定义请求url字符串
        url = 'https://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from' \
              '=mpl_search_suggest&subject=' + quote(type) + '&page=1'
        getType(type, url)


if __name__ == '__main__':
    getTypes()
