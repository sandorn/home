#升级所有可升级的包，使用pip-review
import subprocess
subprocess.call('pip3 install pip-review',shell=True, stdout=subprocess.PIPE)
subprocess.call('pip3 -review --local --interactive --auto',shell=True, stdout=subprocess.PIPE)
    #conda upgrade --all：更新所有包
print('结束')
