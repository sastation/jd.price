#!/usr/bin/env python
# coding:utf-8

import urllib
import json
import re
import codecs
import os

class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        '''
        在初始化中完成所有工作，得到skuid，name，price，执行时间戳
        '''
        # 时间戳
        import datetime
        dts = datetime.datetime.now()
        self.dts = dts.strftime('%y%m%d%H%M')

        self.url = url
        self._response = urllib.urlopen(self.url)
        self.html = self._response.read()

        self.name = self.get_product_name()
        self.skuid = self.get_product_skuid()
        self.price = self.get_product_price()

    def get_product(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        """
        product_re = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(product_re, self.html)[0]
        return product_info

    def get_product_skuid(self):
        """
        通过获取的商品信息，获取商品的skuid
        """
        product_info = self.get_product()
        skuid_re = re.compile(r'skuid: (.*?),')
        skuid = re.findall(skuid_re, product_info)[0]
        return skuid

    def get_product_name(self):
        """
        通过获取的商品信息，获取商品的name
        """
        #'\u4e2d\u6587'.decode('unicode-escape') （你可能需要print它才能看到结果）
        product_info = self.get_product()
        #源码中名称左右有两个',所以过滤的时候应该去掉
        name_re = re.compile(r"name: '(.*?)',")
        name = re.findall(name_re, product_info)[0]
        name = name.decode('unicode-escape') #将其转换为中文
        return name

    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        """
        price = None
        #通过httpfox检测得知，每次网页都会访问这个网页去提取价格嵌入到html中
        #url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'
        #url = 'http://p.3.cn/prices/get?type=1&area=1_72_2799&callback=cnp&skuid=J_' + skuid
        url = 'http://p.3.cn/prices/get?type=1&area=1_72_2799&skuid=J_' + self.skuid

        #json调整格式，并将其转化为utf-8，列表中只有一个字典元素所以取出第一个元素就转化为字典
        price_json = json.load(urllib.urlopen(url))[0]

        #p对应的价格是我们想要的
        if price_json['p']:
            price = price_json['p']
        return price

def get_urls(filename = './jd.urls'):
    lines = []
    f = codecs.open(filename, 'r', 'utf-8')
    for line in f.readlines():
        if line.startswith('#'): continue # 若是注解，则路过本行
        line = line.strip().split(',', 1)[0]
        lines.append(line)
    f.close()
    return lines

if __name__ == '__main__':
    file_name = './jd.urls'
    urls = get_urls(file_name)

    fu = codecs.open(file_name+'.tmp', 'w', 'utf-8')
    fp = codecs.open('jd.price', 'a', 'utf-8')
    for url in urls:
        jp = JdPrice(url)
        #print ("%s, %s, %s, %s") % (jp.dts, jp.skuid, jp.price, jp.name)
        fp.write(("%s, %s, %s, %s\n") % (jp.dts, jp.skuid, jp.price, jp.name))
        fu.write("%s, %s\n" % (jp.url, jp.name))
    fu.close()
    fp.close()

    try:
        os.remove(file_name+'.bak')
    except OSError:
        pass
        
    os.rename(file_name, file_name+'.bak')
    os.rename(file_name+'.tmp', file_name)