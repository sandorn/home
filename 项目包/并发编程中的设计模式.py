# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-01-21 14:25:31
LastEditTime : 2025-01-21 14:25:48
FilePath     : /CODE/项目包/并发编程中的设计模式.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, Set


@dataclass
class WorkEvent:
    """工作事件数据类"""

    event_type: str
    payload: Any
    source_id: str = None
    target_id: str = None
    correlation_id: str = str(uuid.uuid4())


class EventDrivenWorker:
    def __init__(self, worker_id: str):
        """初始化事件驱动工作者"""
        self.worker_id = worker_id
        self.event_handlers: Dict[str, Set[Callable]] = {}
        self.event_queue = asyncio.Queue()
        self.running = False

    async def start(self):
        """启动工作者"""
        self.running = True
        await self._event_loop()

    def subscribe(self, event_type: str, handler: Callable):
        """订阅特定类型的事件"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = set()
        self.event_handlers[event_type].add(handler)

    async def publish(self, event: WorkEvent):
        """发布事件到事件队列"""
        await self.event_queue.put(event)

    async def _event_loop(self):
        """事件处理主循环"""
        while self.running:
            try:
                event = await self.event_queue.get()
                if event.event_type in self.event_handlers:
                    handlers = self.event_handlers[event.event_type]
                    await asyncio.gather(*[handler(event) for handler in handlers])
                self.event_queue.task_done()
            except Exception as e:
                print(f"事件处理异常: {e}")


class EventDrivenSystem:
    def __init__(self):
        """初始化事件驱动系统"""
        self.workers: Dict[str, EventDrivenWorker] = {}
        self.event_bus = asyncio.Queue()
        self.running = False

    async def add_worker(self, worker: EventDrivenWorker):
        """添加工作者到系统"""
        self.workers[worker.worker_id] = worker
        asyncio.create_task(worker.start())

    async def start(self):
        """启动事件系统"""
        self.running = True
        await self._event_dispatcher()

    async def _event_dispatcher(self):
        """事件分发器"""
        while self.running:
            try:
                event = await self.event_bus.get()
                if event.target_id:
                    if event.target_id in self.workers:
                        await self.workers[event.target_id].publish(event)
                else:
                    # 广播事件给所有工作者
                    await asyncio.gather(
                        *[worker.publish(event) for worker in self.workers.values()]
                    )
                self.event_bus.task_done()
            except Exception as e:
                print(f"事件分发异常: {e}")

    async def publish_event(self, event: WorkEvent):
        """发布事件到系统总线"""
        await self.event_bus.put(event)

    def shutdown(self):
        """关闭系统"""
        self.running = False
        for worker in self.workers.values():
            worker.running = False


"""
并发编程中的设计模式
https://mp.weixin.qq.com/s/GWcZr3gG4Puog6f4ObYDHg
事件驱动设计模式
"""
if __name__ == "__main__":

    async def handle_event(event: WorkEvent):
        """事件处理器"""
        print(f"事件处理器: {event}")

    async def main():
        """主函数"""
        system = EventDrivenSystem()
        worker1 = EventDrivenWorker("worker1")
        worker2 = EventDrivenWorker("worker2")
        worker1.subscribe("task", handle_event)
        worker2.subscribe("task", handle_event)
        await system.add_worker(worker1)
        await system.add_worker(worker2)
        await system.start()
        await system.publish_event(WorkEvent("task", "任务1"))
        await system.publish_event(WorkEvent("task", "任务2"))
        await asyncio.sleep(1)
        system.shutdown()

    asyncio.run(main())
