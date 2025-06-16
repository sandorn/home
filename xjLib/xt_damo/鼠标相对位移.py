# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-30 11:35:10
LastEditTime : 2025-05-30 16:09:24
FilePath     : /CODE/xjLib/xt_damo/鼠标相对位移.py
Github       : https://github.com/sandorn/home
==============================================================
# 相对位移`dm.MoveR`测试

- 相对位移的误差问题
"""
from bdtime import tt

from damo import DM

dm = DM()


# ---------------- mouse simulation ---------------
print(f"Mouse position: {dm.position}")  # 当前鼠标位置

# xy_ls = [[100, 10], [1700, 10]]
# for i in range(20):
#     if tt.stop_alt("x"):
#         msg = "*** 暂停!"
#         # raise IOError(msg)
#         print(msg)
#         break

#     xy_i = i % len(xy_ls)
#     xy_v = xy_ls[xy_i]

#     dm.MoveTo(*xy_v)
#     tt.sleep(0.1)

#     dm.RightClick()
#     tt.sleep(0.2)


xy_ls = [[10, 0], [10, 0], [10, 0], [-10, 0], [-10, 0], [-10, 0]]
x_ls = []
for i in range(20):
    if tt.stop_alt('x'):
        msg = "*** 暂停!"
        # raise IOError(msg)
        print(msg)
        break

    xy_i = i % len(xy_ls)
    xy_v = xy_ls[xy_i]
    dm.move_r(*xy_v)

    x_i = dm.position[0]
    x_ls.append(x_i)
    delta_x = 0 if len(x_ls) < 2 else x_ls[-1] - x_ls[-2]
    print(f'--- {i} --- \t Mouse position: {x_i}, \t target_x: {xy_v}, \t delta_x: {delta_x}')

    tt.sleep(0.1)

