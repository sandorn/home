# 检索需要升级的库，逐个升级

import subprocess
import time  # 引入time模块

print("检查已经安装库:")
# pip显示需要更新的python列表
com_list = 'conda list '
print("执行命令并返回结果")
p = subprocess.Popen(
    com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 取命令返回结果，结果是一个二进制字符串，包含了我们上面执行conda list后展现的所有内容
out = p.communicate()[0]
print("二进制转utf-8字符串")
out = str(out, 'utf-8')

print("切出待升级的包名, 并存入列表")
need_back = []
for i in out.splitlines()[4:]:
    临时字符 = i.split(' ')[0]
    print("----------备份{} -----------".format(临时字符))
    need_back.append(临时字符)

ticks = time.time()
filename = 'conda-data%s.txt' % (ticks)
print(filename)
print("写库名到备份文件")
file = open(filename, 'w')
sep = '\n'
file.write(str(sep.join(need_back)))
file.close()
print("{}个库已全部备份完毕！".format(len(need_back)))
