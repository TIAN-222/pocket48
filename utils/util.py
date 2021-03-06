# -*- coding: utf-8 -*-
import time
import random
import re
import urllib
import hashlib
import requests
import json


def convert_timestamp_to_timestr(timestamp):
    """
    将13位时间戳转换为字符串
    :param timestamp:
    :return:
    """
    timeArray = time.localtime(timestamp / 1000)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return time_str


def convert_timestr_to_timestamp(time_str):
    """
    将时间字符串转换为时间戳
    :param time_str:
    :return:
    """
    timestamp = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    return timestamp


def random_str(strs):
    return random.choice(strs)


# 过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


# 替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"',
                     }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def replace(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def make_signature(post_fields):
    """
    生成调用微打赏接口所需的签名

    PHP的例子：
        $post_fields = $_POST;
        ksort($post_fields);
        $md5_string = http_build_query($post_fields);
        $sign = substr(md5($md5_string), 5, 16);

    :param post_fields: post请求的参数
    :return:
    """
    post_fields_sorted = ksort(post_fields)
    md5_string = urllib.urlencode(post_fields_sorted) + '&p=das41aq6'
    print md5_string
    sign = hashlib.md5(md5_string).hexdigest()[5:21]
    print sign
    return sign


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


if __name__ == '__main__':
    # strs = filter_tags("""
    # test<span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tu-65768ccc23.png\" style=\"width:1em;height:1em;\" alt=\"[吐]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_haha-bdd6ceb619.png\" style=\"width:1em;height:1em;\" alt=\"[哈哈]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tu-65768ccc23.png\" style=\"width:1em;height:1em;\" alt=\"[吐]\"></span><span class=\"url-icon\"><img src=\"//h5.sinaimg.cn/m/emoticon/icon/others/l_xin-8e9a1a0346.png\" style=\"width:1em;height:1em;\" alt=\"[心]\"></span><br/><a class='k' href='https://m.weibo.cn/k/test?from=feed'>#test#</a>
    # """)
    # print strs
    url = 'https://wds.modian.com/api/project/orders'
    post_fields = {
        "pro_id": 10289,
        "page": 1,
    }
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4033.400 QQBrowser/9.7.12622.400'}
    sign = make_signature(post_fields)
    post_fields['sign'] = sign

    r = requests.post(url, post_fields, headers=header)
    print r.text
