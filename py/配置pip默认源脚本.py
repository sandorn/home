
#!/usr/bin/python
# coding: utf-8

import platform
import os

os_type = platform.system()
if "Linux" == os_type:
    fileDirPath = "%s/.pip" % os.path.expanduser('~')
    filePath = "%s/pip.conf" % fileDirPath
    if not os.path.isdir(fileDirPath):
        os.mkdir(fileDirPath)
    fo = open(filePath, "w")
    fo.write(
        "[global]\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple/\n[install]\ntrusted-host=pypi.tuna.tsinghua.edu.cn\n")
    fo.close()
    print "Configuration is complete"
elif "Windows" == os_type:
    fileDirPath = "%s\\pip" % os.path.expanduser('~')
    filePath = "%s\\pip.ini" % fileDirPath
    if not os.path.isdir(fileDirPath):
        os.mkdir(fileDirPath)
    fo = open(filePath, "w")
    fo.write(
        "[global]\nindex-url=https://pypi.tuna.tsinghua.edu.cn/simple/\n[install]\ntrusted-host=pypi.tuna.tsinghua.edu.cn\n")
    fo.close()
    print "Configuration is complete"
else:
    exit("Your platform is unknow!")
