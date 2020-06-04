# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
上传正常，下载无外链
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-13 15:08:09
@LastEditors: Even.Sand
@LastEditTime: 2019-05-13 18:32:21

'''
import requests
import time
from qiniu import Auth, put_file  # , etag


class UploadDownload:
    def __init__(self):
        self.bucket_name = "san3"  # 上传的空间名称
        self.access_key = 'ZhgvxIaC6Rol7fThRR0FdYrnqxTtY14B6kxrYVxq'
        self.secret_key = '0XEqYD5v9aS8OWl7IypohCEIbaLk4vlh4vc1KffD'
        self.domain_prefix = 'http://prfkm4qm7.bkt.clouddn.com/'

    # 下载图片
    def download_image(self, url):
        # urlretrieve用于将远程数据下载到本地 time.time()用于获取时间戳
        image_name = str(int(time.time()))
        # key = str(hash("logo.png")) + ".png"
        r = requests.get(url, "d:/%s.jpg" % image_name)
        assert r.status_code == 200
        return "d:/" + image_name + ".jpg"

    # 上传图片到七牛云存储
    def upload_image(self, file_path):
        # 构建鉴权对象,需要填写你的 Access Key 和 Secret Key
        q = Auth(self.access_key, self.secret_key)
        # 生成上传 Token，可以指定过期时间等。第一个参数是指上传到哪个bucket，第二个参数值保存到七牛的文件的名称
        image_name = str(int(time.time())) + '.jpg'
        token = q.upload_token(self.bucket_name, image_name, 3600)
        # 要上传文件的本地路径。第二个参数是保存到七牛的文件的名称，第三个参数为要上传的文件的完整路径
        info = put_file(token, image_name, file_path)
        if info[1].status_code == 200:
            return self.domain_prefix + image_name
        return None


# 文件名


def main():
    # 创建UploadDownload对象，包含3个属性
    ud = UploadDownload()
    # 调用ud对象的下载图片方法
    # image_name = ud.download_image('http://prfkm4qm7.bkt.clouddn.com/-1502552308539575074.png')
    image_name = 'd:/16.jpg'
    # 图片上传
    res = ud.upload_image(image_name)
    print(res)


if __name__ == '__main__':
    main()

'''---------------------
import subprocess
popen = subprocess.Popen('qrsctl.exe listprefix myworld ""', shell=True, stdout=subprocess.PIPE)
out = popen.stdout.readlines()
for line in out:
    a=str(line.strip())[2:-1]
    cmd="qrsctl.exe get myworld "+a+" "+a
    open = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#命令行辅助工具(qrsctl)_工具_对象存储 - 七牛开发者中心
#https://developer.qiniu.com/kodo/tools/1300/qrsctl
#windwos恢复被七云牛坑的图片 - 王嘟嘟的博客 - CSDN博客
#https://blog.csdn.net/qq_36869808/article/details/85157417

---------------------
作者：anAlgorithmDog
来源：CSDN
原文：https://blog.csdn.net/cxx05260/article/details/87461727

python入门实践六：下载图片并上传七牛云 - 简书
https://www.jianshu.com/p/e242ce830bbd

如何获取存储文件的外链接 - 七牛开发者中心
https://developer.qiniu.com/kodo/kb/1321/how-to-acquire-the-outside-storage-file-links

带你玩转七牛云存储——高级篇 - 王磊的博客 - CSDN博客
https://blog.csdn.net/sufu1065/article/details/80739970

python文件上传与七牛云存储 - 简书
https://www.jianshu.com/p/7363740c6b5e
'''
