import ast
from collections import OrderedDict

import requests
from task.utils.selector.selector import SelectorABC as FatherSelector

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestsSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    #如果requestdata不为空，就用post方法
    def get_html(self, url, headers, requestdata):
        if headers:
            header_dict = ast.literal_eval(headers)
            if type(header_dict) != dict:
                raise Exception('必须是字典格式')

            if requestdata=='':
                r = requests.get(url, headers=header_dict, timeout=30, verify=False)
            else:
                try:#如果requestdata是字典格式，就不用转换
                    requestdata_dict = ast.literal_eval(requestdata)
                except:
                    requestdata_dict = requestdata
                if type(requestdata_dict) != dict:
                    raise Exception('requestdata必须是字典格式')
                r = requests.post(url, headers=header_dict, timeout=30, verify=False, json=requestdata_dict)
        else:
            if requestdata=='':
                r = requests.get(url, timeout=30, verify=False)
            else:
                try:#如果requestdata是字典格式，就不用转换
                    requestdata_dict = ast.literal_eval(requestdata)
                except:
                    requestdata_dict = requestdata
                if type(requestdata_dict) != dict:
                    raise Exception('requestdata必须是字典格式')
                r = requests.post(url, timeout=30, verify=False, json=requestdata_dict)
        r.encoding = r.apparent_encoding
        html = r.text
        return html

    def get_by_xpath(self, url, selector_dict, headers=None, requestdata=None):
        html = self.get_html(url, headers, requestdata)

        result = OrderedDict()
        for key, xpath_ext in selector_dict.items():
            result[key] = self.xpath_parse(html, xpath_ext)
            #去除result中的换行符及空格
            result[key] = result[key].replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', '')

        return result

    def get_by_css(self, url, selector_dict, headers=None, requestdata=None):
        html = self.get_html(url, headers, requestdata)

        result = OrderedDict()
        for key, css_ext in selector_dict.items():
            result[key] = self.css_parse(html, css_ext)
            #去除result中的换行符
            result[key] = result[key].replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', '')
        return result

    def get_by_json(self, url, selector_dict, headers=None, requestdata=None):
        html = self.get_html(url, headers, requestdata)
        html = html.replace('({"resp', '{"resp').replace('":{}}})', '":{}}}')  # .replace后的代码解决了标普出错

        result = OrderedDict()
        for key, json_ext in selector_dict.items():
            result[key] = self.json_parse(html, json_ext)
            result[key] = result[key].replace('[', '').replace(']', '').replace('"', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', '') #.replace后代码为了去掉jsonpath检测方式的“[]”，去除result中的换行符

        return result
