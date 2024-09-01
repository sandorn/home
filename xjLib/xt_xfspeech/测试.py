# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-08-30 15:56:22
LastEditTime : 2024-08-30 15:59:25
FilePath     : /CODE/xjLib/xt_xfspeech/测试.py
Github       : https://github.com/sandorn/home
==============================================================
https://ai.unisound.com/doc/ttslong/WebAPI.html
"""

# -*- coding:utf-8 -*-
import hashlib
import json
import time

import requests

appkey = "**********************"
secret = "**********************"
tts_text = "云知声专注于物联网人工智能服务，是一家拥有完全自主知识产权、世界顶尖智能语音技术的人工智能企业。公司成立于2012年6月，总部位于北京，在上海、深圳、厦门、合肥设有子公司，目前员工接超过500人。"
start_url = "http://ltts.hivoice.cn/start"
progress_url = "http://ltts.hivoice.cn/progress"


class Client:
    def get_sha256(self, timestamp):
        hs = hashlib.sha256()
        hs.update((appkey + timestamp + secret).encode("utf-8"))
        signature = hs.hexdigest().upper()
        return signature

    def do_ttsflow(self):
        self.final_tts_end = 0
        self.start_tts_time = 0  # 发送文本结束时间
        self.send_text_time = 0
        self.first_interval_time = 0
        self.code = 1
        self.task_id = ""
        self.rec_count = 0
        self.total_interval_time = 0
        headers = {"Content-Type": "application/json"}
        ##1.发送文本，记录开始时间，记录成功、失败
        print("start url:", start_url)
        timestamp = str(int(time.time() * 1000))
        start_params = {
            "time": timestamp,
            "sign": self.get_sha256(timestamp),
            "appkey": appkey,
            "text": tts_text,
            "vcn": "kiyo-base",
            "format": "wav",
        }

        print("start param", start_params)
        start_resp = requests.post(
            url=start_url, data=json.dumps(start_params), headers=headers
        )
        start_result = json.loads(start_resp.content)
        print("start result", start_result)
        start_code = start_result.get("error_code")
        task_id = start_result.get("task_id")
        print("task_id=", task_id)
        ##2.查询是否合成结束，记录结束时间，5万20分钟，记录成功、失败
        if (start_code == 0) and task_id:
            while True:
                time.sleep(1)
                progress_timestamp = str(int(time.time() * 1000))
                progress_params = {
                    "time": progress_timestamp,
                    "sign": self.get_sha256(progress_timestamp),
                    "appkey": appkey,
                    "task_id": task_id,
                }
                print("progress param", progress_params)
                progress_resp = requests.post(
                    url=progress_url, data=json.dumps(progress_params), headers=headers
                )
                progress_result = json.loads(progress_resp.content)
                print("progress result", progress_result)
                progress_code = progress_result.get("error_code")
                # 出错
                if progress_code != 0:
                    print("progress error", task_id, progress_code)
                    break
                # 未出错
                progress_task_id = progress_result.get("task_id")
                progress_task_status = progress_result.get("task_status")
                if "done" == progress_task_status:
                    audio_address = progress_result.get("audio_address")
                    break
            print("audio_address ", audio_address)
            # 下载语音
            print("start download ")
            download_response = requests.get(audio_address)
            audio = download_response.content
            download_file_name = "./" + str(int(time.time() * 1000)) + ".wav"
            with open(download_file_name, "wb") as downloadCode:
                downloadCode.write(audio)
            print("download end ", download_file_name)
        else:
            print("start error,error_code ", start_code)
        return self.code


if __name__ == "__main__":
    client = Client()
    client.do_ttsflow()
