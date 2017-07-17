from Login import *
import urllib.request
import urllib
import urllib.error
import urllib.parse
import pymongo
import time


def post_weibo():
    user = Login('weibo_spider@126.com', 'weibospider')
    user.login()

    db = pymongo.MongoClient().weibodata
    rank = db.sortedplace
    places = rank.find()
    first = places[0]['地点']
    second = places[1]['地点']
    third = places[2]['地点']
    fourth = places[3]['地点']
    fifth = places[4]['地点']


    content = ''.join(['最近上海微博签到人数最多的地点~在此~\n第一：',first,'\n第二：',second,'\n第三：',third,'\n第四：',fourth,'\n第五：',fifth,'\n小伙伴们要来玩的话可以优先考虑这些地方哟~'])
    post_data = {
        "location": "v6_content_home",
        "text": content,
        "appkey": "",
        "style_type": "1",
        "pic_id": "",
        "pdetail": "",
        "rank": "0",
        "rankid": "",
        "module": "stissue",
        "pub_source": "main_",
        "pub_type": "dialog",
        "_t": "0"
    }
    post = urllib.parse.urlencode(post_data).encode('utf-8')
    headers = {
        "Referer": "http://weibo.com/u/6058180728/home",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    timer = int(time.time() * 1000)
    url = 'http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd='+str(timer)
    try:
        request = urllib.request.Request(url=url, data=post, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        #print(html)
        print("发布成功！")
    except urllib.error as e:
        print(e.code)


def main():
    post_weibo()


if __name__ == '__main__':
    main()
