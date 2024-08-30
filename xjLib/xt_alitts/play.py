# !/usr/bin/env python
"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:50
LastEditTime : 2022-12-03 16:19:00
FilePath     : /xjLib/xt_Alispeech/xt_Pygame.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import wave
from io import BytesIO
from threading import Thread

import pyaudio
import pygame
from PyQt6.QtCore import QThread, pyqtSignal
from xt_alitts.ex_nss import execute_tts
from xt_thread import thread_print as print


class PlayInThread(Thread):
    """直接播放音频数据"""

    def __init__(self, data, format="wav"):
        super().__init__()
        self._running = True
        self.data = data
        self.format = format
        self.start()

    def run(self):
        print("PlayInThread | Thread_play starting......")
        pygame.mixer.init(frequency=8000)
        if self.format == "wav":
            self.pym = pygame.mixer
            self.pym.Sound(self.data).play()
        else:
            self.pym = pygame.mixer.music
            self.pym.load(BytesIO(self.data)).play()  # type: ignore
        print("PlayInThread | py_mixer new loading......")

        while self.pym.get_busy() and self._running:
            # 正在播放,等待
            QThread.msleep(1000)
            print("PlayInThread | py_mixer.playing......")

    def stop(self):
        self._running = False
        self.pym.stop()
        print("PlayInThread | Stop!!!")

    def as_completed(self):
        self.join()
        self.stop()


class PlayInQThread(QThread):
    """直接播放音频数据"""

    _signal_done = pyqtSignal()

    def __init__(self, data, format="wav"):
        super().__init__()
        self._running = True
        self.data = data
        self.format = format
        self.start()

    def run(self):
        print("PlayInQThread | Qthread_play starting......")
        pygame.mixer.init(frequency=8000)
        if self.format == "wav":
            self.pym = pygame.mixer
            self.pym.Sound(self.data).play()
        else:
            self.pym = pygame.mixer.music
            self.pym.load(BytesIO(self.data)).play()  # type: ignore
        print("PlayInQThread | py_mixer new loading......")

        while self.pym.get_busy() and self._running:
            # 正在播放,等待
            QThread.msleep(1000)
            print("PlayInQThread | py_mixer.playing......")

    def stop(self):
        self._running = False
        self.pym.stop()
        self._signal_done.emit()
        print("PlayInQThread | Stop!!!")

    def as_completed(self):
        self.wait()
        self.stop()


class ThreadPlayText(Thread):
    """文字转语音，并播放"""

    def __init__(self, textlist=None):
        super().__init__()
        self.execute_tts = execute_tts
        self.textlist = textlist or []
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.aformat = "wav"
        self.pym = pygame.mixer

        self.create_vioce()  # 启动语音生成
        self.start()

    def create_vioce(self):
        def __create_vioce():
            while self._running and len(self.textlist) > 0:
                resdata = self.execute_tts(
                    self.textlist.pop(0), readonly=True, aformat=self.aformat
                )
                self.datas_list.extend([item[1] for item in resdata])

            print("ThreadPlayText | ViceFactryMonitor Stop!!!")

        self.ViceFactryMonitor = Thread(
            target=__create_vioce, daemon=True, name="ViceFactryMonitor"
        )
        self.ViceFactryMonitor.start()

    def run(self):
        print("ThreadPlayText | starting......")
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(1000)
                print("ThreadPlayText | py_mixer.playing......")
                continue

            elif len(self.datas_list) > 0:
                # 朗读完毕,有未加载数据
                print("ThreadPlayText | py_mixer new loading......")
                _data = self.datas_list.pop(0)
                pygame.mixer.Sound(_data).play()
                QThread.msleep(20)
                continue

            elif (
                not self.ViceFactryMonitor.is_alive()
                and len(self.textlist) == 0
                and len(self.datas_list) == 0
            ):
                self.stop()
                print("QThreadPlayText | all recod play finished!!!!")

    def stop(self):
        self._running = False
        self.pym.stop()
        print("ThreadPlayText | Stop!!!")

    def as_completed(self):
        self.join()
        self.stop()


class QThreadPlayText(QThread):
    """文字转语音，并播放"""

    _signal_done = pyqtSignal()

    def __init__(self, texts=None):
        super().__init__()
        self.execute_tts = execute_tts
        self.textlist = texts or []
        self.datas_list = []
        self._running = True

        pygame.mixer.init(frequency=8000)  # @不可默认
        self.aformat = "wav"
        self.pym = pygame.mixer

        self.create_vioce()  # 启动语音生成

    def create_vioce(self):
        def __create_vioce():
            while self._running and len(self.textlist) > 0:
                text = self.textlist.pop(0)
                resdata = self.execute_tts(text, readonly=True, aformat=self.aformat)
                self.datas_list.extend([item[1] for item in resdata])

            print("QThreadPlayText | ViceFactryMonitor Stop!!!")

        # #daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self.ViceFactryMonitor = Thread(
            target=__create_vioce, daemon=True, name="ViceFactryMonitor"
        )
        self.ViceFactryMonitor.start()

    def run(self):
        print("QThreadPlayText | starting......")
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(1000)
                print("QThreadPlayText | py_mixer.playing......")
                continue

            elif len(self.datas_list) > 0:
                # 朗读完毕,有未加载数据
                _data = self.datas_list.pop(0)
                pygame.mixer.Sound(_data).play()
                QThread.msleep(20)
                print("QThreadPlayText | py_mixer new loading......")
                continue

            elif (
                not self.ViceFactryMonitor.is_alive()
                and len(self.textlist) == 0
                and len(self.datas_list) == 0
            ):
                print("QThreadPlayText | all recod play finished!!!!")
                self.stop()
                self._signal_done.emit()

    def stop(self):
        self._running = False
        self.pym.stop()
        print("QThreadPlayText | Stop!!!")

    def as_completed(self):
        self.wait()
        self.stop()


def create_read_thread(meta):
    """type完全动态构建类"""

    def __init__fn(self, textlist=None):
        meta.__init__(self)
        self.__dict__["__isQ"] = meta == QThread
        self.__dict__["execute_tts"] = execute_tts
        self.__dict__["textlist"] = textlist or []
        self.__dict__["datas_list"] = []
        self.__dict__["_running"] = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.__dict__["aformat"] = "wav"
        self.__dict__["pym"] = pygame.mixer

        self.create_vioce()  # 启动语音生成
        self.start()

    def create_vioce(self):
        def _create_vioce():
            while self._running and len(self.textlist) > 0:
                text = self.textlist.pop(0)
                resdata = self.execute_tts(text, readonly=True, aformat=self.aformat)
                self.datas_list.extend([item[1] for item in resdata])

            print(f"{meta}_ReadText | ViceFactryMonitor Stop!!!")

        self.ViceFactryMonitor = Thread(
            target=_create_vioce, daemon=True, name="ViceFactryMonitor"
        )
        self.ViceFactryMonitor.start()

    def run(self):
        print(f"{meta}_ReadText | py_mixer starting......")
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(2000)
                print(f"{meta}_ReadText | py_mixer.playing......")
                continue

            elif len(self.datas_list) > 0:
                # 朗读完毕,有未加载数据
                _data = self.datas_list.pop(0)
                pygame.mixer.Sound(_data).play()
                QThread.msleep(20)
                print(f"{meta}_ReadText | py_mixer new loading......")
                continue

            elif (
                not self.ViceFactryMonitor.is_alive()
                and len(self.textlist) == 0
                and len(self.datas_list) == 0
            ):
                self.stop()
                if self.__isQ:
                    self._signal_done.emit()
                print(f"{meta}_ReadText | all recod play finished!!!!")

    def stop(self):
        self._running = False
        self.pym.stop()
        print(f"{meta}_ReadText | Stop!!!")

    def as_completed(self):
        if self.__isQ:
            self.wait()
        else:
            self.join()
        self.stop()

    return type(
        f"Synt_Read_{"QThread" if meta is QThread else "Thread"}",
        (meta,),
        {
            "_signal_done": pyqtSignal() if meta == QThread else None,
            "__init__": __init__fn,
            "create_vioce": create_vioce,
            "run": run,
            "stop": stop,
            "as_completed": as_completed,
        },
    )


Synt_Read_Thread = create_read_thread(Thread)
Synt_Read_QThread = create_read_thread(QThread)


def record_audio(filename, duration, sample_rate=44100, channels=2, chunk=1024):
    """录制音频并保存为.wav文件"""
    audio_format = pyaudio.paInt16
    frames = []

    print("开始录制音频...")
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=audio_format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )

    try:
        for i in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
    except Exception as e:
        print("录制音频出现异常:", e)
    finally:
        print("录制完成！")
        stream.stop_stream()
        stream.close()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    print("音频已保存为", filename)


def play_audio(filename):
    """加载并播放.wav文件"""
    chunk = 1024
    audio = pyaudio.PyAudio()
    wf = wave.open(filename, "rb")

    formats = audio.get_format_from_width(wf.getsampwidth())
    channels = wf.getnchannels()
    rate = wf.getframerate()

    stream = audio.open(
        format=formats, channels=channels, rate=rate, input=True, output=True
    )

    print("开始播放音频...")
    try:
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
    except Exception as e:
        print("播放音频时出现错误:", e)
    finally:
        print("播放完成！")
        stream.stop_stream()
        stream.close()
        audio.terminate()


class MyPyaudioPlayer:
    def __init__(self):
        self._running = True
        self.audio_p = pyaudio.PyAudio()
        self.stream = self.audio_p.open(
            rate=16000,  # 采样率
            channels=1,  # 设置通道数
            format=pyaudio.paInt16,  # 设置采样大小和格式
            output=True,  # 指定为输出流
            # input=True,  # 指定输入流
        )
        print("MyPyaudioPlayer 准备完毕...")

    def stop(self, wait=0):
        QThread.msleep(wait)
        self._running = False
        self.stream.stop_stream()
        self.stream.close()  # 关闭音频流，释放PortAudio系统资源
        self.audio_p.terminate()  # 终止PyAudio对象，释放占用的系统资源
        print("MyPyaudioPlayer Stop!!!")

    def play(self, data):
        def __play():
            print("MyPyaudioPlayer playing...")
            chunk_length_ms = 100  # 每块20ms
            chunks = [
                data[i : i + chunk_length_ms]
                for i in range(0, len(data), chunk_length_ms)
            ]
            for chunk in chunks:
                if not self._running:
                    QThread.msleep(20)
                    break
                else:
                    self.stream.write(chunk)

        self.playthread = Thread(target=__play, name="Play")
        self.playthread.start()


class QThreadPyaudioText(QThread):
    _signal_done = pyqtSignal()

    def __init__(self, texts=None):
        super().__init__()
        self.execute_tts = execute_tts
        self.textlist = texts or []
        self.datas_list = []
        self.chunks = []
        self._running = True
        self.aformat = "wav"
        self.audio_p = pyaudio.PyAudio()
        self.stream = self.audio_p.open(
            rate=16000,  # 采样率
            channels=1,  # 设置通道数
            format=pyaudio.paInt16,  # 设置采样大小和格式
            output=True,  # 指定为输出流
        )
        self.create_vioce()  # 启动语音生成
        print("QThreadPyaudioText 准备完毕...")

    def create_vioce(self):
        def __create_vioce():
            while self._running and len(self.textlist) > 0:
                text = self.textlist.pop(0)
                resdata = self.execute_tts(text, readonly=True, aformat=self.aformat)
                self.datas_list.extend([item[1] for item in resdata])

            print("QThreadPyaudioText | ViceFactryMonitor Stop!!!")

        self.ViceFactryMonitor = Thread(
            target=__create_vioce, daemon=True, name="ViceFactryMonitor"
        )
        self.ViceFactryMonitor.start()

    def run(self):
        print("QThreadPyaudioText | starting......")
        while self._running:
            if len(self.chunks) > 0:
                self.stream.write(self.chunks.pop(0))
                continue

            elif len(self.chunks) == 0 and len(self.datas_list) > 0:
                print("QThreadPyaudioText | new loading......")
                _data = self.datas_list.pop(0)
                chunk_length_ms = 100  # 每块100ms
                self.chunks = [
                    _data[i : i + chunk_length_ms]
                    for i in range(0, len(_data), chunk_length_ms)
                ]
                continue

            elif (
                not self.ViceFactryMonitor.is_alive()
                and len(self.textlist) == 0
                and len(self.datas_list) == 0
                and len(self.chunks) == 0
            ):
                print("QThreadPyaudioText | all recod play finished!!!!")
                self.stop()
                self._signal_done.emit()

    def play(self, data):
        def __play():
            print("MyPyaudioPlayer playing...")
            chunk_length_ms = 100  # 每块100ms
            chunks = [
                data[i : i + chunk_length_ms]
                for i in range(0, len(data), chunk_length_ms)
            ]
            for chunk in chunks:
                if not self._running:
                    break
                else:
                    self.stream.write(chunk)

        self.playthread = Thread(target=__play, name="Play")
        self.playthread.start()

    def stop(self, wait=0):
        QThread.msleep(wait)
        self._running = False
        self.stream.stop_stream()
        self.stream.close()  # 关闭音频流，释放PortAudio系统资源
        self.audio_p.terminate()  # 终止PyAudio对象，释放占用的系统资源
        print("QThreadPyaudioText Stop!!!")

    def as_completed(self):
        self.wait()
        self.stop()


if __name__ == "__main__":
    text_list = [
        "2022世界杯小组赛C组第二轮,阿根廷2:0力克墨西哥,重新掌握出线主动权。第64分钟,梅西世界波破门,打入个人世界杯第8个进球,进球数追平马拉多纳。",
        "第87分钟,恩索·费尔南德斯锁定胜局！目前,波兰积4分,阿根廷和沙特同积3分,阿根廷以净胜球优势排名第二,墨西哥积1分。",
    ]

    def m1():
        QTa = QThreadPlayText(texts=text_list)
        QTa.run()

    def m2():
        out_file = execute_tts(text_list, readonly=True, aformat="wav")
        mypp = MyPyaudioPlayer()
        mypp.play(out_file[0][1])
        mypp.stop(3000)

    def m3():
        RR = QThreadPyaudioText(text_list)
        RR.run()
        # RR.stop(3000)

    m3()
