from wxpy import *
import csv

addfriend_request = '加好友'  #自动添加好友的条件
admin_request_name = '微信名'    #定义管理员微信名（必须是机器人的好友）  ps：raw_content字段需要自己手动更改微信名，微信号
admin_request_num = 'weixinhao'   #定义管理员微信号（必须是机器人的好友）
invite_text = "Helo!回复'功能 + 数字'获取对应功能\n1.我要加群\n2.我要加入协会\n3.我要购买鞋子\n4.了解我们\n5.我需要帮助\n例如：要获取我要加群的功能时回复\n\n功能1"  #任意回复获取的菜单
group_name = '17中南轮滑协会萌新裙'    #定义要查找群的名字
menu_1 = '功能1'   #菜单选项1 定义加群的条件
menu_2 = '功能2'  #菜单选项2
menu_3 = '功能3'  #菜单选项3
menu_4 = '功能4'  #菜单选项4  
menu_5 = '功能5'  #菜单选项5 
csv_1 = 'test.csv'   #表格1


bot = Bot(cache_path = True)
bot.enable_puid()  #启用聊天对象的puis属性
xiaoi = XiaoI('PQunMu3c66bM', 'FrQl1oi1YzpDSULeAIit')   #小i机器人接口
adminer = bot.friends(update=True).search(admin_request_name)[0]
my_group = bot.groups(update=True).search(group_name)[0]
group_admin = my_group.members.search(admin_request_name)[0]


admin_puids = frozenset(['XX', 'YY'])   #不可变集合
admins = list(map(lambda x: bot.friends().search(puid=x), admin_puids))

def invite(user):
    groups = sorted(bot.groups(update=True).search(group_name),
                    key=lambda x: x.name)   #sorted用于排序，lambda x:x.name用于群名排序
    if len(groups) > 0:
        for group in groups:
            if len(group.members) == 500:
                continue    
            if user in group:
                content = "您已经加入了{} [微笑]".format(group.nick_name)   #经过format格式化的内容传递到{}
                user.send(content)
            else:
                group.add_members(user, use_invitation=True)
            return
        else:
            next_topic = group_tmpl.format(re.search(r'\d+', s).group() + 1)  #当前群的名字后面+1
            new_group = bot.create_group(admins, topic=next_topic)
            #以上3句代码的解释为：利用for if else语句进行判断，如果从查找的群名里面找不到对应的群就自动创建一个新群并添加进去
    else:
        print('Invite Failed')

#写表函数
def table(user, text):
    #提取用户的文本，把有用的写入表里
    msg_text = text
    tables = msg_text.split('\n')
    table_name = tables[1].split(':')[1]
    table_stu_num = tables[2].split(':')[1]
    table_phone_num = tables[3].split(':')[1]
    table_department = tables[4].split(':')[1]
    table_list = [table_name, table_stu_num, table_phone_num, table_department, '等待缴费']
    user.send('请稍等，后台处理中')
    with open(csv_1, 'r') as f:   #检查表里是否有登记的学号
        fr_csv = csv.reader(f)
        for row in fr_csv:
            if table_stu_num in row:
                user.send('报名失败，该学号已经登记过了')
                break
        else:
            with open(csv_1, 'a') as f:          #写入表
                fw_csv = csv.writer(f)
                fw_csv.writerow(table_list)
            with open(csv_1, 'r') as f:          #查看是否写入成功
                fr_csv = csv.reader(f)
                for row in fr_csv:
                    if table_stu_num in row:
                        user.send('报名成功,请回复‘支付宝’或者‘微信’进行支付')
                        break
                else:
                    user.send('报名失败，请重新报名或者联系管理员')

#查询表函数
def check(user, text):
    check_text = text.split(':')[1]
    with open(csv_1, 'r') as f:
        fr_csv = csv.reader(f)
        for row in fr_csv:
            if check_text in row:
                user.send('登记信息如下，如有疑问请联系管理员')
                user.send('学号:'+row[1]+"\n缴费情况:"+row[-1])
                break
        else:
            user.send('暂无学号登记记录')   

# 注册好友请求类消息
@bot.register(msg_types=FRIENDS,enabled=True)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if addfriend_request in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('机器人自动接受了你的请求,你可以任意回复获取功能菜单，若机器人没回复菜单则表明机器人尚未工作，请等待')

#注册自动回复好友消息
@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    if menu_1 in msg.text.lower():
        invite(msg.sender)
    elif menu_2 in msg.text.lower():
        content_2_1 = "请复制下面的模板回复\nps：部门可以多填，如果是技术部和Hockey就填写 部门：技术部、Hockey\n填写示例：\n姓名：小明\n学号：111111111\n电话：18888888888\n部门：技术部"
        content_2_2 = "报名表\n姓名:\n学号:\n电话:\n部门:"
        msg.sender.send(content_2_1)
        msg.sender.send(content_2_2)
    elif menu_3 in msg.text.lower():
        return '购买鞋子功能测试中' #跟报名的功能差不多就不写了。。。
    elif menu_4 in msg.text.lower():
        msg.sender.send('关注公众号可以了解更多')
        msg.sender.send_raw_msg(
        # 名片的原始消息类型
        raw_type=42,
        # 注意 `username` 在这里应为微信 ID，且被发送的名片必须为自己的好友
        raw_content='<msg username="zdnflunhua" nickname="中大南方RNF"/>'
        )   
    elif menu_5 in msg.text.lower():
        return '我要帮助功能测试中'     #最初设想是返回从公众号获取的素材，结果没有相对应的Api。只能返回图片，语音，或者文本了，不过这个就一行代码的事，就不写了
    elif '报名表' in msg.text.lower():
        table(msg.sender, msg.text)
    elif '支付宝' in msg.text.lower():
        msg.sender.send('请进入支付宝扫描二维码支付，备注姓名，电话\n支付完成后请第二天回复“查询:+学生号“查询情况\n示例：\n查询:111111111')
        msg.sender.send('二维码生成中')
        msg.sender.send_image('zfb.png')
    elif '微信' in msg.text.lower():
        msg.sender.send('请进入微信扫描二维码支付，备注姓名，电话\n支付完成后请第二天回复“查询:+学生号“查询情况\n示例：\n查询:111111111')
        msg.sender.send('二维码生成中')
        msg.sender.send_image('wx.png')
    elif '查询' in msg.text:
        check(msg.sender, msg.text)
    elif '管理员' in msg.text:
        msg.sender.send('请添加名片联系管理员')
        msg.sender.send_raw_msg(
        # 名片的原始消息类型
        raw_type=42,
        # 注意 `username` 在这里应为微信 ID，且被发送的名片必须为自己的好友
        raw_content='<msg username="bc9526" nickname="陈思煜"/>'
        )   
    else:
        return invite_text 

#处理管理员信息
@bot.register(adminer, msg_types=TEXT)
def adminer(msg):
    if '备份' in msg.text:
        msg.sender.send_file('test.csv')
    else:
        return "请检查命令是否输入正确"    

#群聊管理
@bot.register(my_group, msg_types=TEXT)
def group(msg):
    if msg.is_at :
        if '踢出' in msg.text:
            if msg.member == group_admin :
                for member_name in msg.text.split('@')[2:]:
                    print(member_name)
                    re_name = my_group.members.search(member_name)[0].remove()
                    print(re_name)
                    msg.sender.send("已经移出:"+member_name)
            else:
                return "你不是管理员不能进行踢人操作"
        else:
            xiaoi.do_reply(msg)     
bot.join()                           
