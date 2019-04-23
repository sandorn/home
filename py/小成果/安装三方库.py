# 安装库
import subprocess

import win32ui

dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
dlg.SetOFNInitialDir('d:/')  # 设置打开文件对话框中的初始显示目录
dlg.DoModal()

filename = dlg.GetPathName()  # 获取选择的文件名称
# print(filename)

list1 = []
with open(filename, 'r') as file:
    list1 = file.readlines()

for i in range(0, len(list1)):
    list1[i] = list1[i].rstrip('\n')
    print(list1[i])

s = len(list1)
n = 1
print("{}个库开始安装：".format(s))
for nu in list1:
    com_ins = 'pip install {py}'.format(py=nu)
    print("共有{}个库，正在安装第{}个库{}，\n执行命令：{}，请耐心等待.......".format(s, n, nu, com_ins))
    # p = subprocess.Popen(com_ins,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen(
        com_ins, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0]
    n += 1
    print("----------{com} 执行结束-----------\n".format(com=com_ins))

print("{}个库已全部安装完毕！".format(s))
'''
pip freeze > requirements.txt #输出本地包环境至文件
pip install requirements.txt #根据文件进行包安装
#########################################################
conda clean -p      //删除没有用的包
conda clean -t      //tar打包
conda clean -y -all //删除所有的安装包及cache
conda list         #查看已经安装的文件包
conda list  -n xxx       #指定查看xxx虚拟环境下安装的package
conda update xxx   #更新xxx文件包
conda uninstall xxx   #卸载xxx文件包

# 更新conda，保持conda最新
conda update conda 
# 更新anaconda
conda update anaconda 
# 更新python
conda update python
# 假设当前环境是python 3.4, conda会将python升级为3.4.x系列的当前最新版本
conda update anaconda-navigator    //update最新版本的anaconda-navigator
conda update -n base conda        //update最新版本的conda

conda create -n xxxx python=3.5   //创建python3.5的xxxx虚拟环境
conda activate xxxx               //开启xxxx环境
conda deactivate                  //关闭环境
conda env list                    //显示所有的虚拟环境

# 删除一个已有的环境
conda remove --name python34 --all
# 安装xxxx
conda install xxxx
# 查看当前环境下已安装的包
conda list
# 查看某个指定环境的已安装包
conda list -n python34
# 查找package信息
conda search numpy

# 安装package
conda install -n python34 numpy # 如果不用-n指定环境名称，则被安装在当前活跃环境 也可以通过-c指定通过某个channel安装
# 更新package
conda update -n python34 numpy
# 删除package
conda remove -n python34 numpy


# 添加Anaconda的TUNA镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
# TUNA的help中镜像地址加有引号，需要去掉
# 设置搜索时显示通道地址
conda config --set show_channel_urls yes

#更新所有包
conda update --all
conda upgrade --all
conda clean -p      #删除没有用的包
'''
