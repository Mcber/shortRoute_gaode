# -*- coding: utf-8 -*-

import requests
import json
import urllib
import re
import csv
import os
from bs4 import BeautifulSoup

_KEY1 = '619ed12d1faba843409f7e4733b69374'
_KEY2 = 'a7a748325a547459c5611ea4449e01ba'
_KEY3 = '36485fd9cf9d4865138d746840a6dba5'
_KEY4 = '96bd5c85e3e9b7602d8f6dd4a2650ae8'

def get_route(origin, destination, city='020', strategy='0', nightflag='0', time='8:00', output='json', key=_KEY4):
    URL = 'https://restapi.amap.com/v3/direction/transit/integrated'
    # URL_all = 'https://restapi.amap.com/v3/direction/transit/integrated?origin={}&destination={}&city={}&strategy={}&nightflag={}&time={}&output={}&key={}'.format(origin, destination, city, strategy, nightflag, time, output, key)
    # print URL_all
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'guid=387f-f537-21ab-dd33; UM_distinctid=1657e657646b55-05b354dc69c0de-34677908-1aeaa0-1657e65764776b; cna=mokFFHi42VcCATr45ZUv3em3; passport_login=MjE4OTYxOTQ3LGFtYXBCTVR6aXc4N1IseW12OGpnbjY0NTgyb3BocGo4bXkyaG8zeWdycnltMmcsMTUzNTYxMDA5NixPR1V3TnpKak1XSmtObUppWWpsak9EZzROakk1TlRRME56STBPVGxoTWpVPQ%3D%3D; dev_help=t%2FS%2BjSKdYmbqy5SgYcOjPTk2NjkyMzgwZWEyNjE1NjVjYTVhZDkwOTQ3N2NhMjNmMzYyOTM3ODYxMjg4Yzc2YzI3MzRkMWI1MmZlNGJjNjZXFRdLYqMZkZXiqQ%2FvNmJUwzKwMm9ZaD7wcJGUG1t2Uzuj3z8ridEG3jSffd8sxDDQ3bl7VEqwgLFn2133AnYvxu0%2BqGLrSD66z4aJr9odn1UF7hhv0RKl9RhEnA3B2Jo%3D; isg=BJGRzA2XrieSkMIwVkmSxEkloJvrVhoV-94pRHMkbNvZGrZsu00mQqqzuK5ZEp2o',
        'Host': 'restapi.amap.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    data = {
        'origin': origin,                   # 出发点坐标，不能有空格
        'destination': destination,         # 目的地坐标，不能有空格
        'city': city,                       # 起点城市数值代号
        'strategy': strategy,               # 公交换乘策略
        'nightflag': nightflag,             # 是否计算夜班车
        'time': time,                       # 预计出发时间
        'output': output,                   # 返回数据格式类型
        'key': key,                         # 用户的key
    }
    response = requests.post(url= URL, headers=headers,data=data)
    jsonData = json.loads(response.content)

    transits = jsonData['route']['transits']
    for transit in transits:
        del transit['segments']
        del transit['missed']

    return transits


def get_location(address, city='020', output='json', key=_KEY4):
    info = []
    URL = 'https://restapi.amap.com/v3/geocode/geo'
    # URL_all = 'https://restapi.amap.com/v3/geocode/geo?address={}&city=020&output=XML&key=619ed12d1faba843409f7e4733b69374'.format(ad)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'guid=387f-f537-21ab-dd33; UM_distinctid=1657e657646b55-05b354dc69c0de-34677908-1aeaa0-1657e65764776b; cna=mokFFHi42VcCATr45ZUv3em3; passport_login=MjE4OTYxOTQ3LGFtYXBCTVR6aXc4N1IseW12OGpnbjY0NTgyb3BocGo4bXkyaG8zeWdycnltMmcsMTUzNTYxMDA5NixPR1V3TnpKak1XSmtObUppWWpsak9EZzROakk1TlRRME56STBPVGxoTWpVPQ%3D%3D; dev_help=t%2FS%2BjSKdYmbqy5SgYcOjPTk2NjkyMzgwZWEyNjE1NjVjYTVhZDkwOTQ3N2NhMjNmMzYyOTM3ODYxMjg4Yzc2YzI3MzRkMWI1MmZlNGJjNjZXFRdLYqMZkZXiqQ%2FvNmJUwzKwMm9ZaD7wcJGUG1t2Uzuj3z8ridEG3jSffd8sxDDQ3bl7VEqwgLFn2133AnYvxu0%2BqGLrSD66z4aJr9odn1UF7hhv0RKl9RhEnA3B2Jo%3D; isg=BJGRzA2XrieSkMIwVkmSxEkloJvrVhoV-94pRHMkbNvZGrZsu00mQqqzuK5ZEp2o',
        'Host': 'restapi.amap.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }


    data = {
        'address': address,
        'city': city,
        'output': output,
        'key': key,
    }

    try:
        response = requests.post(url=URL, headers=headers, data=data)

        jsonData = json.loads(response.content)
        full_address = jsonData['geocodes'][0]['formatted_address']
        location = jsonData['geocodes'][0]['location']

        info = [location,full_address]

        return info

    except:

        return ['0','0']


def get_station_name():
    URL = 'http://cs.gzmtr.com/base/doLoadLines.do'

    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_36fe4ad5dc620a3949163bcfa0ea56e5=1536068591; Hm_lpvt_36fe4ad5dc620a3949163bcfa0ea56e5=1536068591; JSESSIONID=7572DD18CC4FA1A0BE42BBC5F2683DB4.tomcat_mtr_8081; Hm_lvt_718d62b72db64b1e29f91933a1dd6e03=1536068608; Hm_lpvt_718d62b72db64b1e29f91933a1dd6e03=1536068608',
        'Host': 'cs.gzmtr.com',
        'Referer': 'http://cs.gzmtr.com/ckfw/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'callback': 'jQuery18000925518945685746_1536069030086',
        '_': '1536069030089',
    }

    response = requests.post(url=URL, headers=headers, data=data)


    pattern = re.compile(r'.+?\((.*)\)')
    j = re.match(pattern,response.content).group(1)

    jsonData = json.loads(j)

    stageName = []
    for i in jsonData['lines']:

        for j in i['stages']:
            stageName.append([i['lineName'], j['stageName']])

    with open('stageName.csv','wb') as n:
        csv_Writer = csv.writer(n)
        for l in stageName:

            line = l[0].encode('utf-8')
            station = l[1].encode('utf-8')

            full_station = u'{}地铁站'.format(l[1])
            info = get_location(full_station)

            if info[0] == '0':
                full_station = u'{}(地铁站)'.format(l[1])
                info = get_location(full_station)

            # print info
            location = info[0].encode('utf-8')
            full_name = info[1].encode('utf-8')

            print line, station, location, full_name

            csv_Writer.writerow([line, station, location, full_name])

def writeCsv(filename, msg_list, mode='a+'):
    with open(filename, mode) as f:
        csv_writer = csv.writer(f)
        encode_list = []
        for _ in msg_list:
            encode_list.append(_.encode('utf-8'))
        csv_writer.writerow(encode_list)



def get_bus_station_name(filename):
    if os.path.exists(filename):
        os.remove(filename)
    URL_allbus = 'http://guangzhou.gongjiao.com/lines_all.html'
    response_allbus = requests.post(url=URL_allbus)            # 获取bus的路线名和跳转的url
    soup = BeautifulSoup(response_allbus.content, 'html.parser')

    find_list = soup.find_all(name='ul', attrs={'class': 'f-cb'})[1]            # 通过绝对的list位置获取bus路线的list,可能会出错
    bus_list = find_list.find_all(name='a')
    bus_info = {}
    for l in bus_list:
        bus_info[l['href']] = l.string

    count = 0
    for url in bus_info.keys():
        url_bus = url
        response_station = requests.post(url=url_bus)           # 获取每条线的站名
        soup_station = BeautifulSoup(response_station.content, 'html.parser')
        find_list = soup_station.find_all(name='ul', attrs={'class': 'gj01_line_img JS-up clearfix'})[0]
        station_list = find_list.find_all(name='a')         # 获取该线路的所有站名的list
        for sta in station_list:
            msg_list = [bus_info.get(url),sta.text] + get_location(u'{}公交站'.format(sta.text))          # 线路名，站名，站坐标，站全名
            writeCsv(filename, msg_list)          # 写入每行的bus站点信息
            print msg_list[3]  # 输出bus信息
            count += 1

    print count


def calRoute(mid_location, destination1, destination2):
    result1 = {}
    result2 = {}
    duration1 = []
    duration2 = []
    try:
        route1 = get_route(mid_location, destination1)
        route2 = get_route(mid_location, destination2)

        for r1 in route1:
            duration1.append(r1['duration'])

        for r2 in route2:
            duration2.append(r2['duration'])

        duration1.sort()            # 对得到的路程时间排序
        duration2.sort()

        for r1 in route1:
            if r1['duration'] == duration1[0]:          # 获取最短时间的路线
                result1 = r1

        for r2 in route2:
            if r2['duration'] == duration2[0]:          # 获取最短时间的路线
                result2 = r2

        count_result = str(int(duration1[0]) + int(duration2[0])).decode()

        result = {u'results': count_result, u'result1': result1, u'result2': result2}

        return result

    except:
        return {}

def main():
    rr_location = '113.347798,23.008095'
    mm_location = '113.339457,23.126010'
    station_list = []
    results_list = []

    with open('stageName.csv', 'rb') as n:
        reader = csv.reader(n)
        for line in reader:
            station_list.append(line)

    for s in station_list:

        try:
            result = calRoute(s[2], rr_location, mm_location)
            # print result
            times = str(float(result['results']) / 60).decode('utf-8')
            time1 = str(float(result['result1']['duration']) / 60).decode('utf-8')
            time2 = str(float(result['result2']['duration']) / 60).decode('utf-8')
            distance1 = str(float(result['result1']['distance']) / 1000).decode('utf-8')
            distance2 = str(float(result['result2']['distance']) / 1000).decode('utf-8')
            walking_distance1 = str(float(result['result1']['walking_distance']) / 1000).decode('utf-8')
            walking_distance2 = str(float(result['result2']['walking_distance']) / 1000).decode('utf-8')
            cost1 = result['result1']['cost']
            cost2 = result['result2']['cost']
            nightflag1 = result['result1']['nightflag']
            nightflag2 = result['result2']['nightflag']

            format_result = [times, time1, distance1, walking_distance1, cost1, nightflag1, time2, distance2, walking_distance2, cost2, nightflag2]
        except:
            format_result = [u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', ]


        s_code = [c.decode('utf-8') for c in s]

        print s_code[3], format_result
        info_list = s_code+format_result

        count = len(results_list)
        if count > 0:
            i = count-1
            # j = i-1
            key = info_list

            while i >= 0:
                if i == 0 and float(results_list[i][4]) >= float(key[4]):
                    results_list.insert(i, key)
                    break

                if float(results_list[i][4]) <= float(key[4]):
                    results_list.insert(i + 1, key)
                    break

                i -= 1

        else:
            results_list.append(info_list)

    # for _ in results_list:
    #     print _[4]

    with open('results3.csv', 'wb') as r:
        writer = csv.writer(r)
        csv_header = [u'线路', u'站名', u'坐标', u'全地名', u'总时间/分', u'时间1/分', u'距离1/千米', u'行走距离1/千米', u'费用1/元', u'夜班1',
                      u'时间2/分', u'距离2/千米', u'行走距离2/千米', u'费用2/元', u'夜班2',]

        writer.writerow([h.encode('utf-8') for h in csv_header])
        for l in results_list:
            # print l
            try:
                writer.writerow([f.encode('utf-8') for f in l])
            except:
                print l


    print 'finished!!'


if __name__ == '__main__':

    # main()
    get_bus_station_name('busStationName.csv')