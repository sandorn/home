# coding=utf-8
class Family(object):
    def __init__(self, name):
        self.name = name
    def call_name(self):
        return self.name

if __name__ == "__main__":
    a = Family("Tom").call_name()
    b = Family("Tom").call_name()
    c = Family("Jerry")
    d = Family("Jerry")
    # print a is b  # 判断a 对象是b
    # print a == b # 判断a 的值与b值相等
    # print c is d
    # print c == d

class A():
    pass
class B(A):
    pass

print (isinstance(A(), A))  # isinstance(object,classinfo)
print (isinstance(B(),A))
aa =1
bb ='string'
cc=(1,2)
print (isinstance(aa, int))
print (isinstance(bb, str))
print (isinstance(cc,(int,str,list,tuple)))
print (type(aa)==int)
print (type(aa))


'''
params = ["爱加倍","70周岁"]
sel_sql = "select * from {0[0]} where 保险期间 = {0[1]}"
sp_sql=sel_sql.format(params)
print(sp_sql)
'''
