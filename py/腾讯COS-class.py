# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-13 17:41:47
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 15:59:48


tencentyun/cos-python-sdk-v5
https://github.com/tencentyun/cos-python-sdk-v5
对象存储 快速入门 - SDK 文档 - 文档中心 - 腾讯云
https://cloud.tencent.com/document/product/436/12269
cos-python-sdk-v5/demo.py at master · tencentyun/cos-python-sdk-v5
https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

cos-python-sdk-v5/cos_client.py at 0116356f00742c7c641e3868157c88ae42a37583 · tencentyun/cos-python-sdk-v5
https://github.com/tencentyun/cos-python-sdk-v5/blob/0116356f00742c7c641e3868157c88ae42a37583/qcloud_cos/cos_client.py
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# from qcloud_cos import CosServiceError
# from qcloud_cos import CosClientError
import time
import sys
import logging


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


# 文件名


def main():
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


if __name__ == '__main__':
    main()
