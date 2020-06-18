# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-12 15:49:16
#FilePath     : /xjLib/xt_DAO/test/__doc__.py
#LastEditTime : 2020-06-12 15:50:05
#Github       : https://github.com/sandorn/home
#==============================================================
'''


'''
    fiter举例：
    query(User.name).filter(User.fullname==’Ed Jones’)
    query.filter(or_(User.name == ‘ed’, User.name == ‘wendy’))
    query.filter(and_(User.name == ‘ed’, User.fullname == ‘Ed Jones’))

    filters = {
        User.name == ‘fengyao’,
        User.age > 25
    }
    User.query.filter(*filters).first()

    #查询 user 表里面名字等于 Tom 的：
    db.session.query(User).filter(User.name == 'Tom').all()
    #查询 user 表里面名字等于 Tom 并且年龄等于 18：
    db.session.query(User).filter(User.name == 'Tom', User.age == 18).all()
    #也可以这样：
    db.session.query(User).filter(User.name == 'Tom'）.filter(User.age == 18).all()
    #如果想使用 and 拼接需要用以下方式：
    db.session.query(User).filter(and_(User.name == 'Tom', User.age == 18)).all()
    #以下的方式 and 后面的 User.age == 18 不会生效：
    db.session.query(User).filter(User.name == 'Tom' and User.age == 18).all()
    #查询 user 表里面名字等于 Tom 的或者年龄等于 18：
    db.session.query(User).filter(or_(User.name == 'Tom', User.age == 18)).all()
    #查询 user 表里面名字等于 Tom 的并且年龄大于 18
    db.session.query(User).filter(User.name == 'Tom', User.age > 18).all()
    #查询 name 中包含字母 a 的所有数据(模糊查询)
    db.session.query(User).filter(User.name.like('%{0}%'.format("a"))).all()

    常用的SQLAlchemy字段类型
    类型名	python中类型	说明
    Integer	int	普通整数，一般是32位
    SmallInteger	int	取值范围小的整数，一般是16位
    BigInteger	int或long	不限制精度的整数
    Float	float	浮点数
    Numeric(P，D)decimal.Decimal	定点数
        P：有效数字长度。范围是1~65。
        D是表示小数点后的位数。范围是0~30。MYSQL要求D<=P。

    VARCHAR	str
    String	str	变长字符串
    Text	str	变长字符串，对较长或不限长度的字符串做了优化
    Unicode	unicode	变长Unicode字符串
    UnicodeText	unicode	变长Unicode字符串，对较长或不限长度的字符串做了优化
    Boolean	bool	布尔值
    Date	datetime.date	时间
    Time	datetime.datetime	日期和时间
    LargeBinary	str	二进制文件
    TIMESTAMP  自动获取时间

    1. Integer：整型，映射到数据库中是int类型。
    2. Float：浮点类型，映射到数据库中是float类型。它占据的32位。
    3. Double：双精度浮点类型，映射到数据库中是double类型，占据64位。
    4. String：可变字符类型，映射到数据库中是varchar类型。
    5. Boolean：布尔类型，映射到数据库中的是tinyint类型。
    6. DECIMAL：定点类型。是专门为了解决浮点类型精度丢失的问题的。在存储钱相关的字段的时候建议大家都使用这个数据类型。并且这个类型使用的时候需要传递两个参数，第一个参数是用来标记这个字段总能能存储多少个数字，第二个参数表示小数点后有多少位。
    7. Enum：枚举类型。指定某个字段只能是枚举中指定的几个值，不能为其他值。在ORM模型中，使用Enum来作为枚举。
    8. Date：存储时间，只能存储年月日。映射到数据库中是date类型。在Python代码中，可以使用`datetime.date`来指定。
    9. DateTime：存储时间，可以存储年月日时分秒毫秒等。映射到数据库中也是datetime类型。在Python代码中，可以使用`datetime.datetime`来指定。
    10. Time：存储时间，可以存储时分秒。映射到数据库中也是time类型。在Python代码中，可以使用`datetime.time`来指定。
    11. Text：存储长字符串。一般可以存储6W多个字符。如果超出了这个范围，可以使用LONGTEXT类型。映射到数据库中就是text类型。
    12. LONGTEXT：长文本类型，映射到数据库中是longtext类型。

    常用的SQLAlchemy列选项
    选项名	说明
    primary_key	如果为True，代表表的主键
    unique	如果为True，代表这列不允许出现重复的值
    index	如果为True，为这列创建索引，提高查询效率
    nullable	如果为True，允许有空值，如果为False，不允许有空值
    default	为这列定义默认值

    常用的SQLAlchemy关系选项
    选项名	说明
    backref	在关系的另一模型中添加反向引用
    primaryjoin	明确指定两个模型之间使用的联结条件
    uselist	如果为False，不使用列表，而使用标量值
    order_by	指定关系中记录的排序方式
    secondary	指定多对多中记录的排序方式
    secondaryjoin	在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件

    one_or_none()和one()很像，除了在查询不到的时候。查询不到的时候one_or_none()会直接返回None，但是在找到多个值的时候和one()一样。

    query.scalar()援引自one()函数，查询成功之后会返回这一行的第一列参数

    https://www.jianshu.com/p/0ad18fdd7eed
    https://blog.csdn.net/q370835062/article/details/84974951
    http://www.pythontip.com/blog/post/12611/
'''
