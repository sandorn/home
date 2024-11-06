import asyncio
import functools

from xt_requests import get


def get_html(url, **kwargs):
    return get(url, **kwargs)


async def main():
    loop = asyncio.get_running_loop()

    # 使用 functools.partial  传递关键字参数
    partial_func = functools.partial(get_html, "https://www.baidu.com", index=30)

    # 在执行器中运行同步函数
    return await loop.run_in_executor(None, partial_func)


# 运行异步主函数
print(1111111111, asyncio.run(main()))
