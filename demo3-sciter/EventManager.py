class EventManager:
    def __init__(self, _Queue, funMap):
        self.__active = False
        self.Queue = _Queue
        self.funMap = funMap

    def __Run(self):
        while self.__active == True:
            try:
                # 获取事件的阻塞时间设为1秒
                event = self.Queue.get(timeout = 1)
                getattr( self.funMap, event['fun'] )( event['msg'] )
            except Exception as e:
                pass

    def Start(self):
        self.__active = True
        self.__Run()

    def Stop(self):
        self.__active = False