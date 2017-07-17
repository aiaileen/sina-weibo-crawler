import pymongo


# 过滤重复数据
def kill_redundant():
    db = pymongo.MongoClient().weibodata.webodata
    data1 = db.find()
    count = data1.count()
    i = 0
    while i < count:
        print(i)
        data0 = data1[int(i)]
        t = i+1
        while t < count:
            next0 = data1[t]
            t += 1
            if data0['微博内容'] == next0['微博内容']:
                if data0['微博ID'] == next0['微博ID']:
                    db.remove(next0)
                    count = count-1
                    print('正在过滤重复')
                else:
                    pass
            else:
                pass
        i += 1


#统计每个地点出现的次数，存入表countplace
def count_place():
    db = pymongo.MongoClient().weibodata
    wbdata = db.weibodata
    cleandb = wbdata.find()
    count = cleandb.count()
    i = 0
    while i < count:
        print(i)
        data0 = cleandb[i]
        a = data0['定位地点']
        counta = wbdata.find({'定位地点': a}).count()
        pcount = db.countplace
        dic = {
            '地点': a,
            '次数': counta
        }
        p = pcount.find()
        pc = p.count()#新表长度
        t = 0
        if pc == 0:
            pcount.insert(dic)
            print('正在存入数据')
            continue
        else:
            while t <= pc:
                pt = p[int(t)]
                if a == pt['地点']:
                    break
                t += 1
                if t == pc:
                    pcount.insert(dic)
                    print('正在存入数据')
        i += 1


#排序 以次数为倒序，然后存入新表sortedplace
def sort_place():
    db = pymongo.MongoClient().weibodata
    pcount = db.countplace
    psort = pcount.find().sort('次数', pymongo.DESCENDING)
    for sort in psort:
        sorted = db.sortedplace #存入新表
        sorted.insert(sort)
        print('正在排序')


#删掉过于笼统及无用数据如机场
def kill_general():
    db = pymongo.MongoClient().weibodata
    sorted = db.sortedplace
    sorted.remove({'地点': '上海'})
    sorted.remove({'地点': '上海·上海浦东国际机场'})
    sorted.remove({'地点': '上海·虹桥机场'})
    sorted.remove({'地点': '上海·上海虹桥国际机场'})
    sorted.remove({'地点': '上海·虹桥火车站'})
    sorted.remove({'地点': '上海·火车站'})
    sorted.remove({'地点': '上海·闵行区'})
    sorted.remove({'地点': '上海·浦东新区'})
    sorted.remove({'地点': '上海·松江区'})
    sorted.remove({'地点': '上海·青浦区'})
    sorted.remove({'地点': '上海·金山区'})
    sorted.remove({'地点': '上海·宝山区'})
    sorted.remove({'地点': '上海·徐汇区'})
    sorted.remove({'地点': '上海·黄浦区'})
    sorted.remove({'地点': '上海·嘉定区'})
    sorted.remove({'地点': '上海·长宁区'})
    sorted.remove({'地点': '上海·静安区'})
    sorted.remove({'地点': '上海·普陀区'})
    sorted.remove({'地点': '上海·虹口区'})
    sorted.remove({'地点': '上海·杨浦区'})
    sorted.remove({'地点': '上海·奉贤区'})
    sorted.remove({'地点': '上海·崇明区'})


def main():
    kill_redundant()
    count_place()
    sort_place()
    kill_general()

if __name__ == '__main__':
    main()
