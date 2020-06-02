name_list=['alex','eric','rain','xxx']

#通过序列项迭代
for i in name_list:
    print(i)

print('')
#通过序列索引迭代
for x in range(len(name_list)):
    print('index is %s,name is %s' %(x,name_list[x]))


print('')
#基于enumerate的项和索引
for y,name in enumerate(name_list,2):
    print('index is %s,name is %s' %(y,name))
