import json
from urllib.request import urlopen, quote


def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '8K1QyhtvTH0pfzCwGP2HxQYTlyL4vuzF'
    add = quote(address)  # 由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)  # 对json数据进行解析
    return temp
