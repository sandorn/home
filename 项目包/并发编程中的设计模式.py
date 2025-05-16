# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-01-21 14:25:31
LastEditTime : 2025-05-12 10:38:23
FilePath     : /CODE/项目包/并发编程中的设计模式.py
Github       : https://github.com/sandorn/home
==============================================================
"""

# ? 生产者-消费者模式

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Set


@dataclass
class WorkEvent:
    """工作事件数据类"""

    event_type: str
    payload: Any
    source_id: str = ""
    worker_id: str = ""
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class EventDrivenWorker:
    def __init__(self, worker_id: str):
        """初始化工人"""
        self.worker_id = worker_id
        self.event_handlers: Dict[str, Set[Callable]] = {}
        self.event_queue = asyncio.Queue()
        self.running = False
        print(f"{self.worker_id} 工人初始化......")

    async def start(self):
        """启动工人"""
        self.running = True
        await self._event_loop()
        print(f"启动 {self.worker_id} 工人待命......")

    def subscribe(self, event_type: str, handler: Callable):
        """订阅特殊指令"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = set()
        self.event_handlers[event_type].add(handler)
        print(f"{self.worker_id} 工人订阅特殊指令:{event_type}。")

    async def publish(self, event: WorkEvent):
        """发布任务到任务队列"""
        await self.event_queue.put(event)
        print(f"向 {self.worker_id} 工人下达任务指令......")

    async def _event_loop(self):
        """任务处理循环"""
        while self.running:
            try:
                event = await self.event_queue.get()
                print(f"工人: {self.worker_id} | 接收到任务: {event}")
                if event.event_type in self.event_handlers:  # 特殊指令
                    handlers = self.event_handlers[event.event_type]
                    await asyncio.gather(*[handler(event) for handler in handlers])
                self.event_queue.task_done()
            except Exception as e:
                print(f"工人 任务处理异常: {e}")


class EventDrivenSystem:
    def __init__(self):
        """初始化工场系统"""
        self.workers: Dict[str, EventDrivenWorker] = {}
        self.event_bus = asyncio.Queue()
        self.running = False
        print("工场初始化......")

    async def add_worker(self, worker: EventDrivenWorker):
        """添加工人到工场"""
        self.workers[worker.worker_id] = worker
        print(f"添加工人 {worker.worker_id} 到工场......")
        asyncio.create_task(worker.start())

    async def start(self):
        """启动工场运行"""
        self.running = True
        print("启动工场运行......")
        await self._event_dispatcher_loop()

    async def _event_dispatcher_loop(self):
        """任务分发"""
        while self.running:
            try:
                event = await self.event_bus.get()
                print("工场系统 分发任务......")
                if event.worker_id is not None and event.worker_id in self.workers:
                    # 发布事件到指定工作者
                    print(f"工场系统 分发任务: {event} | 目标: {event.worker_id}")
                    await self.workers[event.worker_id].publish(event)
                else:
                    print(f"工场系统 分发任务: {event} | 目标: {event.worker_id}")
                    # 广播事件给所有工作者
                    await asyncio.gather(
                        *[worker.publish(event) for worker in self.workers.values()]
                    )
                self.event_bus.task_done()
            except Exception as e:
                print(f"工场系统 任务分发异常: {e}")

    async def publish_event(self, event: WorkEvent):
        """发布任务到任务池"""
        await self.event_bus.put(event)
        print("工场系统 发布任务到任务池")

    def shutdown(self):
        """关闭工场"""
        self.running = False
        for worker in self.workers.values():
            worker.running = False
        print("停止工场系统运行！！！")


# 创建事件驱动系统实例
async def main():
    organizer = EventDrivenSystem()
    # 创建工作者
    workers_id = [f"worker_{i}" for i in range(1, 3)]
    worker1 = EventDrivenWorker(workers_id[0])
    worker2 = EventDrivenWorker(workers_id[1])
    # 创建特殊事件类型
    handler_events = ["task_completed", "data_processed"]

    # 定义处理函数（添加完成回调）
    async def handle_task_completed(event: WorkEvent):
        print(
            f"[{datetime.now().isoformat()}]  {worker1.worker_id}  处理任务完成事件: {event.payload}"
        )

    async def handle_data_processed(event: WorkEvent):
        print(
            f"[{datetime.now().isoformat()}]  {worker2.worker_id}  处理数据处理事件: {event.payload}"
        )

    # 订阅事件类型
    worker1.subscribe(handler_events[0], handle_task_completed)
    worker2.subscribe(handler_events[1], handle_data_processed)

    # 启动工场和工人
    asyncio.create_task(organizer.start())  # 启动工场
    await organizer.add_worker(worker1)  # 添加工人
    await organizer.add_worker(worker2)

    # 确保系统初始化完成
    await asyncio.sleep(0.1)

    # 创建测试事件
    events = [
        WorkEvent("task_1", {"task": "月度报告"}, worker_id=workers_id[0]),
        WorkEvent("data_2", {"data": "销售记录"}, worker_id=workers_id[1]),
        WorkEvent("系统通知", {"msg": "已经到中午午休时间，可以休息"}),  # 广播事件
        WorkEvent("紧急通知", {"msg": "时间紧迫，请各位加紧工作！！"}),  # 广播事件
        WorkEvent(handler_events[0], {"task": "季度报告"}, worker_id=workers_id[0]),
        WorkEvent(handler_events[1], {"data": "库存数据"}, worker_id=workers_id[1]),
    ]

    # 批量发布事件
    for event in events:
        await organizer.publish_event(event)

    # 使用队列join等待处理完成（代替sleep）
    await organizer.event_bus.join()  # 等待工场任务安排完毕
    for worker in organizer.workers.values():
        await worker.event_queue.join()  # 等待工人完成任务

    organizer.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
"""
并发编程中的设计模式
https://mp.weixin.qq.com/s/GWcZr3gG4Puog6f4ObYDHg
事件驱动设计模式
"""
