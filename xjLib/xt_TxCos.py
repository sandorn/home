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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-07-16 17:41:43
腾讯对象存储，可以储存文件
'''

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import time
import sys


class txConfig:
    SecretId = 'AKIDV0Xy0fpYzNeEh1SX8e6UipldkjrpgIn7'
    SecretKey = 'PyX0Ocv7bzDHA890ocGoiTfU9zqbBN9q'
    Region = 'ap-beijing'  # 用户的Region地域信息
    # Domain = 'https://snad-1253302746.cos.ap-beijing.myqcloud.com'


class txCos:
    def __init__(self):
        self.Bucket = 'snad-1253302746'
        self.client = CosS3Client(CosConfig(
            Region=txConfig.Region,
            SecretId=txConfig.SecretId,
            SecretKey=txConfig.SecretKey,
        ))

    def __enter__(self, *args):
        print("In __enter__()", args)
        return self

    def __exit__(self, *args):
        print("In __exit__()", args)

    def down(self, file_url_name, LocalFilePath):
        '''获取文件到本地,file_url_name为网络文件名，LocalFilePath为本地文件名'''
        try:
            response = self.client.get_object(
                self.Bucket,
                file_url_name,
            )
            response['Body'].get_stream_to_file(LocalFilePath)
            return response
        except Exception as err:
            print(err)

    def up(self, LocalFilePath):
        '''高级上传接口(推荐)'''
        file_name = str(int(time.time())) + '_' + LocalFilePath.split('/')[-1]
        try:
            response = self.client.upload_file(
                self.Bucket,
                Key=file_name,
                LocalFilePath=LocalFilePath,
                PartSize=10,
                MAXThread=10,
            )
            return response
        except Exception as err:
            print(err)
            pass


if __name__ == '__main__':
    with txCos() as tx:
        print(tx.up('d:/26.png'))
        print(tx.down('1582177854.png', 'd:/28.jpg'))
