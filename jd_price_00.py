#!/usr/bin/env python
# coding:utf-8

import urllib  
import json  
import re  
   
   
class JdPrice(object):  
    """ 
    对获取京东商品价格进行简单封装 
    """  
    def __init__(self, url):  
        self.url = url  
        self._response = urllib.urlopen(self.url)  
        self.html = self._response.read()  
   
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
        return name.decode('unicode-escape')#将其转换为中文  
   
    def get_product_price(self):  
        """ 
        根据商品的skuid信息，请求获得商品price 
        :return: 
        """  
        price = None  
  
        #得到产品的序号和名称，取价格的时候会用得到  
        skuid = self.get_product_skuid()  
        name = self.get_product_name()  
        print name  
          
        #通过httpfox检测得知，每次网页都会访问这个网页去提取价格嵌入到html中  
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'  
          
        #json调整格式，并将其转化为utf-8，列表中只有一个字典元素所以取出第一个元素就转化为字典  
        price_json = json.load(urllib.urlopen(url))[0]  
          
        #p对应的价格是我们想要的  
        if price_json['p']:  
            price = price_json['p']  
        return price  
   
   
  
if __name__ == '__main__':  
    print "+"*20+"welcome to 京东放养的爬虫"+"+"*20    
    url = 'http://item.jd.com/1217524.html'  
    jp = JdPrice(url)  
    print jp.get_product_price()  
    print "+"*20+"welcome to 京东放养的爬虫"+"+"*20  
