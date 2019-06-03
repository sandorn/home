# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-14 09:01:46
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 16:02:21
'''


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import time
import sys


class txCos:
    def __init__(self):
        self.Bucket = 'san3-1253302746'
        self.secret_id = 'AKIDV0Xy0fpYzNeEh1SX8e6UipldkjrpgIn7'  # 替换为用户的secret_id
        self.secret_key = 'PyX0Ocv7bzDHA890ocGoiTfU9zqbBN9q'  # 替换为用户的secret_key
        self.region = 'ap-beijing'  # 替换为用户的region
        self.token = None  # 使用临时秘钥需要传入Token，默认为空,可不填
        self.domain = 'https://san3-1253302746.cos.ap-beijing.myqcloud.com/'
        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token)  # 获取配置对象
        self.client = CosS3Client(self.config)

    def __enter__(self):
        print("In __enter__()")
        return self

    def __exit__(self, args):
        print("In __exit__()")

    # 下载文件
    def down(self, file_name, LocalFilePath):
        #! 文件下载 获取文件到本地,第二个参数为网络文件名(不能写domain)，第三个参数为本地文件名
        response = self.client.get_object(self.Bucket, file_name)
        response['Body'].get_stream_to_file(LocalFilePath)
        return True

    # 上传文件
    def up(self, LocalFilePath):
        # 高级上传接口(推荐)
        file_name = str(int(time.time())) + '.' + LocalFilePath.split('.')[-1]
        response = self.client.upload_file(self.Bucket, Key=file_name, LocalFilePath=LocalFilePath, PartSize=10, MAXThread=10)
        return response['ETag']


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # 创建UploadDownload对象，包含3个属性
    txcoses = txCos()
    # 调用txcoses对象的下载图片方法
    res = txcoses.down('1557742130.jpg', 'd:/26.jpg')
    print(res)
    res = txcoses.up('d:/26.jpg')
    print(res)
    # image_name = 'd:/16.jpg'  # 图片上传
    # res = txcoses.up(image_name)
