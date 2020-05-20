#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from hashlib import md5
import random

"""有道抓取

	1、浏览器F12开启网络抓包,Network-All,页面翻译单词后找Form表单数据
	2、在页面中多翻译几个单词，观察Form表单数据变化（有数据是加密字符串）
	3、刷新有道翻译页面，抓取并分析JS代码（本地JS加密）
	4、找到JS加密算法，用Python按同样方式加密生成加密数据
	5、将Form表单数据处理为字典，通过requests.post()的data参数发送

	1、开启F12抓包，找到Form表单数据
	2、在页面中多翻译几个单词，观察Form表单数据变化
	3、一般为本地js文件加密，刷新页面，找到js文件并分析JS代码
		# 方法1
		Network - JS选项 - 搜索关键词salt
		# 方法2
		控制台右上角 - Search - 搜索salt - 查看文件 - 格式化输出
		​
		# 最终找到相关JS文件 : fanyi.min.js
	4、打开JS文件，分析加密算法，用Python实现

	md5加密
		from hashlib impotr md5
		s=md5()
		s.update('1234'.encode())
		s.hexdigest()"""


# 获取相关加密算法的结果
def get_salt_sign_ts(word):
    # ts
    ts = str(int(time.time() * 1000))
    # salt
    salt = ts + str(random.randint(0, 9))
    # sign
    string = "fanyideskweb" + word + salt + "Nw(nmmbP%A-r6U3EUn]Aj"
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()
    return salt, sign, ts


def attack_yd(word):
    salt, sign, ts = get_salt_sign_ts(word)
    # url为抓包抓到的地址 F12 -> translate_o -> post
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '257',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ntes_nnid=63b693fb5eed4bd47e628884a0b7f84d,1586955311129; OUTFOX_SEARCH_USER_ID_NCOO=179410137.09541598; OUTFOX_SEARCH_USER_ID="-451380417@10.108.160.17"; JSESSIONID=aaaLeoQb9zypc916sUrix; ___rl__test__cookies=1589441366926',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/?keyfrom=fanyi-new.logo',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    # Form表单数据
    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": "524b386317f537e5c682881a938903bb",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }
    json_html = requests.post(url, data=data, headers=headers
                              ).json()
    result = json_html['translateResult'][0][0]['tgt']
    return result


if __name__ == '__main__':
    word = input('请输入要翻译的单词：')
    result = attack_yd(word)
    print(result)
