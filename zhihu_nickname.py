import json
import os
import random
import requests
from lxml import etree
import time
import re
import hashlib
import execjs
import datetime
class Nicknames():
    def __init__(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.offset = 0
        self.x_zse_96=''
        self.cookie=''
        self.url='https://www.zhihu.com/api/v4/members/ren-min-wang/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        if not os.path.exists("zhihunickname.txt"):
            self.txt=open("zhihunickname.txt",encoding='utf8',mode="w")
        else:
            self.txt=open("zhihunickname" + str(nowTime) + ".txt",encoding='utf8',mode="w")
        self.encrypt_str = '2.0_a_S0HbeqQMYf6XY0M8Sq6iuBSMFpHqt0ZCNqc0uBe8FY'
        self.headers = {
            "x-api-version": "3.0.91",
            'x-app-za': 'OS=Web',
            "x-zse-93": "101_3_2.0",
            "x-zse-96": self.encrypt_str,
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Cookie": self.cookie,
        }
    def get_headers(self):
        parse_url ='/' + re.findall(r'[^https://www.zhihu.com]+.*', self.url)[0]
        print(parse_url)
        star = 'd_c0='
        end = ';'
        cookie_mes = 'd_c0="ALDdAx5C1hKPTqd0KT2c1bXDL4LmTxeCCIU=|1616396274";'.replace(star, '')
        cookie_mes = cookie_mes[:cookie_mes.index(end)]
        print(cookie_mes)
        f = "+".join(["101_3_2.0", parse_url, cookie_mes])
        print(f)
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        with open('g_encrypt.js', 'r') as f:
            ctx1 = execjs.compile(f.read(), cwd=r'C:\Users\Administrator\node_modules')
        self.encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
        print(self.encrypt_str)
        self.headers = {
            "x-api-version": "3.0.91",
            'x-app-za': 'OS=Web',
            "x-zse-93": "101_3_2.0",
            "x-zse-96": self.encrypt_str,
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Cookie": self.cookie,
        }
    def request_url(self,indexurl,headers):
        res=requests.get(indexurl,headers=headers)
        print(res.status_code)
        data=json.loads(res.content)
        return data
    def set_next_page(self):
        self.offset = self.offset+20
        next_page="https://www.zhihu.com/api/v4/members/ren-min-wang/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=" + str(self.offset) + "&limit=20"
        self.url=next_page
        return next_page
    def get_nicknames(self,data):
        for i in data['data']:
            nickname=i['name']
            if "知乎" not in nickname:
                self.txt.writelines(nickname+'\n')
                print(nickname)
        return
    def start(self):
        i=1
        pages=input('页数:')
        try:
            while i <= int(pages) :
                data=self.request_url(self.url,self.headers)
                self.set_next_page()
                self.get_headers()
                name=self.get_nicknames(data)
                print('\n以获取第'+str(i)+'页，下一页:'+self.url)
                time.sleep(5)
                i+=1
        except:
            self.txt.close()
        self.txt.close()
if __name__ == "__main__":
    nicknames=Nicknames()
    nicknames.start()
    print("finished!")
            
            
