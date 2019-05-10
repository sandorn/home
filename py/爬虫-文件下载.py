# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   爬虫-文件下载.py
@Time    :   2019/05/06 08:59:45
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
redraiment / Python简易文件上传下载工具
Python简易文件上传下载工具 - 代码片段 - 码云 Gitee.com
https://gitee.com/redraiment/codes/hl7ase6uitjkyzfrvngo352
'''

import BaseHTTPServer
import cgi
import mimetypes
import os
import posixpath
import shutil

if not mimetypes.inited:
    mimetypes.init()


class RESTful(BaseHTTPServer.BaseHTTPRequestHandler):

    exts = mimetypes.types_map.copy()
    exts.update({'': 'application/octet-stream'})

    def mime_type(self, path):
        base, ext = posixpath.splitext(path)
        ext = ext.lower()
        return self.exts[ext] if ext in self.exts else self.exts['']

    def not_found(self):
        self.send_response(404)
        self.end_headers()

    def download(self, filename):
        f = open(filename, 'rb')
        fs = os.fstat(f.fileno())

        content_type = self.mime_type(filename) + "; charset=utf-8"
        content_length = str(fs[6])
        last_modified = self.date_time_string(fs.st_mtime)

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", content_length)
        self.send_header("Last-Modified", last_modified)
        self.end_headers()

        shutil.copyfileobj(f, self.wfile)

        f.close()

    def do_GET(self):
        filename = self.path[1:]
        if os.path.isfile(filename):
            self.download(filename)
        else:
            self.not_found()

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type']
            })
        filename = form['file'].filename
        f = open(filename, 'wb')
        shutil.copyfileobj(form['file'].file, f)
        f.close()

        self.send_response(201)
        self.send_header("Content-Length", "0")
        self.end_headers()


def main():
    from urllib import request
    from urllib.parse import quote
    import string
    print("downloading with urllib")
    url = 'https://www.baidu.com'
    #url = quote(url, safe=string.printable)
    f = request.urlopen(url)
    print(f)
    data = f.read()
    print(data)
    data = data.decode('utf-8')
    print(data)
    #data = unicode(f, 'ascii').encode('UTF-8')
    with open("结果.txt", "wb", encoding='utf-8') as code:
        code.write(data)


#Python网络请求urllib和urllib3详解 - 简书
#https://www.jianshu.com/p/f05d33475c78

if __name__ == '__main__':
    httpd = BaseHTTPServer.HTTPServer(('', 8080), RESTful)
    print("http %s %s" % httpd.socket.getsockname())
    httpd.serve_forever()
