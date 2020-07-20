# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : 域名失效状态，需要更新domain_prefix
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-05-14 10:31:24
#FilePath     : /xjLib/xt_QiniuCos.py
#LastEditTime : 2020-07-16 18:25:30
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import requests
import time
from qiniu import Auth, put_file


class qiniuCos:
    def __init__(self):
        self.bucket_name = "san3"  # 上传的空间名称
        self.access_key = 'ZhgvxIaC6Rol7fThRR0FdYrnqxTtY14B6kxrYVxq'
        self.secret_key = '0XEqYD5v9aS8OWl7IypohCEIbaLk4vlh4vc1KffD'
        self.domain_prefix = 'http://prfkm4qm7.bkt.clouddn.com/'

    # 下载图片
    def down(self, url):
        # urlretrieve用于将远程数据下载到本地 time.time()用于获取时间戳
        image_name = str(int(time.time()))
        # key = str(hash("logo.png")) + ".png"
        r = requests.get(self.domain_prefix + url, "d:/" + image_name + "." + url.split('.')[-1])
        print(r.text)
        assert r.status_code == 200
        return "d:/" + image_name + "." + url.split('.')[-1]

    # 上传图片到七牛云存储
    def up(self, LocalFilePath):
        # 构建鉴权对象,需要填写你的 Access Key 和 Secret Key
        q = Auth(self.access_key, self.secret_key)
        # 生成上传 Token，可以指定过期时间等。第一个参数是指上传到哪个bucket，第二个参数值保存到七牛的文件的名称
        image_name = str(int(time.time())) + '.' + LocalFilePath.split('.')[-1]
        token = q.upload_token(self.bucket_name, image_name, 3600)
        # 要上传文件的本地路径。第二个参数是保存到七牛的文件的名称，第三个参数为要上传的文件的完整路径
        info = put_file(token, image_name, LocalFilePath)
        if info[1].status_code == 200:
            return self.domain_prefix + image_name
        return None


if __name__ == '__main__':
    # 创建UploadDownload对象，包含3个属性
    QN = qiniuCos()
    # 调用QN对象的下载图片方法
    QN.down('1580807450.jpg')
    # image_name = 'd:/26.jpg'
    # 图片上传
    # res = QN.up(image_name)
    # print(res)
