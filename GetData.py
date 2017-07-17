from Login import *
from lxml import etree
import urllib
import urllib.request
import pymongo
import json
import random
import time


class GetData:
    def __init__(self, interval='50', begin_url="http://weibo.com/p/1001018008631000000000000"):
        self.begin_url = begin_url
        self.set_interval(interval)

    def set_interval(self, interval):
        self.interval = int(interval)

    def url(self, i):
        if i == 1:
            return self.begin_url
        if i > 1:
            return self.begin_url + '?current_page=' + str(i + 1 + 2 * (i - 2)) + '&since_id=&page=' + str(i) + '#feedtop'

    def download(self):
        i = 1
        while i < 50:
            url = self.url(i)
            i += 1
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # raw = response.read()
            # with open('raw', r'wb') as f:
            #    f.write(raw)
            raw = response.read().decode()
            lines = raw.splitlines()
            for line in lines:
                if line.startswith('<script>FM.view({"ns":"pl.content.homeFeed.index","domid":"Pl_Third_App__17"'):
                    n = line.find('html":"')
                    if n > 0:
                        html = line[n + 7: -12].replace("\\", "")
                        html1 = bytes(bytearray(html, encoding='utf-8'))
                        page = etree.HTML(html1)  # 初始大页面
                        details = page.xpath('//a[@node-type="feed_list_item_date"]')
                        t = 0  # 第t条数据
                        for detail in details:
                            detailhref = detail.attrib.get('href')
                            # 进入详情页爬取信息
                            rqst = urllib.request.Request(detailhref)
                            rspse = urllib.request.urlopen(rqst)
                            lines1 = rspse.readlines()
                            for line0 in lines1:
                                line1 = line0.strip().decode()
                                if line1.startswith('<script>FM.view({"ns":"pl.content.weiboDetail.index"'):
                                    line11 = line1.strip('<script>FM.view(')
                                    line2 = line11.strip(')</script>')  # 去掉script标签变成json
                                    j = json.loads(line2)
                                    wbdetail0 = j['html']
                                    wbdetail00 = wbdetail0.replace("\n", "")
                                    wbdetail000 = wbdetail00.replace("<br>", ",")
                                    wbdetail = wbdetail000.replace("   ", "")
                                    try:
                                        wb = etree.HTML(wbdetail)
                                        contents = wb.xpath('//div[@class="WB_text W_f14"]/.')  # 微博内容
                                        date = wb.xpath('//a[@node-type="feed_list_item_date"]')  # 微博发布时间
                                        locations = wb.xpath('//i[@class="W_ficon ficon_cd_place"]/..')  # 位置
                                        user = wb.xpath('//a[@class="W_f14 W_fb S_txt1"]')  # 用户信息
                                        pics = wb.xpath('//ul[@node-type="fl_pic_list"]/li/img')
                                        nickname = contents[0].attrib.get('nick-name')
                                        userid0 = user[0].attrib.get('usercard')
                                        userid = userid0.replace("id=", "").replace("&type=0&refer_flag=", "")
                                        userhref = user[0].attrib.get('href')
                                        posttime = date[0].attrib.get('title')
                                        content = contents[0].xpath('string(.)')
                                        location = locations[0].attrib.get('title')
                                        locturl = locations[0].attrib.get('href')
                                        picurl = []
                                        for pic in pics:
                                            picurl0 = pic.attrib.get('src')
                                            picurl.append(picurl0)
                                        if (nickname != 'None' and str(content) != 'None'):
                                            db = pymongo.MongoClient().weibodata
                                            collection = db.aa20170506
                                            #collection = db.wbdata##存入数据集
                                            dic = {
                                                '昵称': nickname,
                                                '微博ID': userid,
                                                '定位地点': location,
                                                '精确坐标': locturl,
                                                '发表时间': posttime,
                                                '微博内容': content,
                                                '博主主页': userhref,
                                                '照片链接': picurl
                                            }
                                            collection.insert(dic)
                                            t = t + 1
                                            print("第" + str(i-1) + "页，第" + str(t) + "条微博爬取完毕")
                                    except Exception:
                                        pass

            sleeptime_one = random.randint(self.interval - 25, self.interval - 15)
            sleeptime_two = random.randint(self.interval - 15, self.interval)
            if i % 2 == 0:
                sleeptime = sleeptime_two
            else:
                sleeptime = sleeptime_one
            print('sleeping ' + str(sleeptime) + ' seconds...')
            time.sleep(sleeptime)


def main():
    user = Login('#usrname', '#pswd')
    user.login()
    data = GetData()
    data.download()

if __name__ == '__main__':
    main()
