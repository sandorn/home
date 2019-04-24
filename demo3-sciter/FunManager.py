from time import time, sleep
from os import path as osPath
import asyncio
import aiohttp
from threading import Thread

class AsyncioDownload(object):
    '''使用协程下载图片'''
    def __init__(self, loop, _GuiRecvMsg, proxies=None ):
        self.GuiRecvMsg = _GuiRecvMsg
        self._session = None
        self.loop = loop
        self.prox = ''.join(('http://', proxies)) if proxies else proxies
        self.timeout = 10
        t = Thread(target=self.start_loop, args=(self.loop,))
        t.setDaemon(True)    # 设置子线程为守护线程
        t.start()

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def __session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self.loop)
        return self._session

    async def stream_download(self, d, _GuiRecvMsgDict):
        try:
            client = self.__session()
            async with client.get( d['http'], proxy=self.prox, timeout=self.timeout) as response:
                if response.status != 200:
                    print('error')
                    return
                print('200',d['id'])
                if not osPath.isfile(d['fpath']):
                    with open(d['fpath'], 'ab') as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
                self.GuiRecvMsg.put(_GuiRecvMsgDict)
        except asyncio.TimeoutError:
            pass

class ServiceEvent(object):
    '''服务进程'''
    def __init__(self, _GuiQueue, cfg):
        self.GuiQueue = _GuiQueue
        self.cfg = cfg
        self.proxies = self.cfg.get('proxies', None)
        self.html = '''
            <div.pic-view imgid='%s'></div>
        '''
        # 主线程中创建一个事件循环
        self.new_loop = asyncio.new_event_loop()
        self.dld = AsyncioDownload(self.new_loop, self.GuiQueue, self.proxies )

    def __run_coroutine_threadsafe(self, data, _GuiRecvMsgDict):
        asyncio.run_coroutine_threadsafe(self.dld.stream_download(
            data,
            _GuiRecvMsgDict
        ), self.new_loop)

    def clickCallBack(self, msg):
        sleep(3)
        self.__putGui( 'clickCallBack', msg )

    def getPicByList(self, msg):
        # 为图片创建占位图
        imgidList = self.__creatPlaceholderImg()
        for imgid in imgidList:
            picHttp = self.cfg['picList'].pop(0)
            file_name = picHttp.split("/")[-1]
            file_path = osPath.join( self.cfg['pic_temp'], file_name )
            # 图片下载完成后需要执行的任务
            _GuiRecvMsgDict = {
                'fun' : 'setImgBg',
                'msg' : {'id':imgid,'fpath':file_path}
            }
            if not osPath.isfile(file_path):
                # 将下载任务动态添加到协程循环中
                self.__run_coroutine_threadsafe(
                    {'id': imgid,'http': picHttp,'fpath': file_path},
                    _GuiRecvMsgDict
                )
            else:
                self.__putGui( 'setImgBg', {'id':imgid,'fpath':file_path} )
        pass

    def __creatPlaceholderImg(self):
        # 先创建5个占位图
        html = ''
        imgidList = []
        time_now = ''
        for i in range(0, 5):
            time_now = '-'.join( ( str(i), str(time()) ) )
            # 储存图片的id
            imgidList.append( time_now )
            html += self.html % ( time_now )
        self.__putGui('creatPlaceholderImg', html)
        return imgidList

    def __putGui(self, f, m = None ):
        self.GuiQueue.put({
            'fun' : f,
            'msg' : m
        })

class GuiCallBack(object):
    def __init__(self, funCall):
        self.funCall = funCall

    def clickCallBack(self, msg):
        return self.funCall('clickCallBack', msg )

    def creatPlaceholderImg(self, msg):
        return self.funCall('creatPlaceholderImg', msg )

    def setImgBg(self, msg):
        return self.funCall('setImgBg', msg )