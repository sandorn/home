#逐个升级所有已经安装的库

import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions

# 如果版本是9.0.1，下面get_installed_distributions后无括号
# 如果版本是10.0.1，下面get_installed_distributions后有括号

n=1
s=len(get_installed_distributions())
for dist in get_installed_distributions():
    call("pip3 install -U " + dist.project_name, shell=True)
    #conda upgrade --all：更新所有包
    print("共有{}个库，正在更新第{}个库{}，请耐心等待.......".format(s,n,dist.project_name))
    n+=1
print("{}个库已全部更新完毕！".format(s))
# 逐个更新，速度较慢
