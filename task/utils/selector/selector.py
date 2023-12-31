import json
from abc import ABCMeta, abstractmethod

import jsonpath
from scrapy.selector import Selector


class SelectorABC():
    __metaclass__ = ABCMeta

    def xpath_parse(self, html, xpath_ext):
        if 'string()' in xpath_ext:
            xpath_ext = xpath_ext.split('/')
            xpath_ext = '/'.join(xpath_ext[:-1])
            res = Selector(
                text=html).xpath(xpath_ext)[0].xpath('string(.)').extract()
        else:
            res = Selector(text=html).xpath(xpath_ext).extract()

        if len(res) != 0:
            return res[0]
        else:
            #raise Exception('无法获取文本信息')
            res = "出错" #出错也通知
            return res

    def css_parse(self, html, css_ext):
        res = Selector(text=html).css(css_ext).extract()

        if len(res) != 0:
            return res[0]
        else:
            #raise Exception('无法获取文本信息')
            res = "出错"
            return res

    def json_parse(self, html, json_ext):
        try:
            resJson = json.loads(html)
        except Exception:
            raise Exception('Json转换错误')
        res = json.dumps(jsonpath.jsonpath(resJson, json_ext),
                         ensure_ascii=False)

        if len(res) != 0:
            return res
        else:
            #raise Exception('无法获取文本信息')
            res = "出错"  #出错也通知
            return res

    @abstractmethod
    def get_by_xpath(self):
        pass

    @abstractmethod
    def get_by_css(self):
        pass

    @abstractmethod
    def get_by_json(self):
        pass
