import xJlib as xx

aaa = '23asa'
bbb = 'kjljl2'


def buggy(arg, result=[]):
    result.append(arg)
    print("变量【{0}】的类型是【{1}】".format(result, xx.getType(result)))
    print(result)


buggy("AAA")
egg = [1, 2, "gg"]
print("变量【{0}】的类型是【{1}】".format(egg, xx.getType(egg)))
buggy("BBB", egg)
print("变量【{0}】的类型是【{1}】".format(egg, xx.getType(egg)))


def buy(arg):
    result = []
    result.append(arg)
    print("变量【{0}】的类型是【{1}】".format(result, xx.getType(result)))
    print(result)


buy("AAA")
buy("BBB")
