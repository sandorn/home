# !/usr/bin/env python

import base64
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import requests
from xt_xfspeech.cfg import CFG

APPID = CFG.APPID.value
APIKey = CFG.APIKey.value
APISecret = CFG.APISecret.value


class TestTask:
    def __init__(self):
        self.host = HOST
        self.app_id = APPID
        self.api_key = APIKey
        self.api_secret = APISecret

    # 生成鉴权的url
    def assemble_auth_url(self, path):
        params = self.assemble_auth_params(path)
        # 请求地址
        request_url = f"http://{self.host}{path}"
        return f"{request_url}?{urlencode(params)}"

    # 生成鉴权的参数
    def assemble_auth_params(self, path):
        # 生成RFC1123格式的时间戳
        format_date = format_date_time(mktime(datetime.now().timetuple()))
        # 拼接字符串
        signature_origin = f"host: {self.host}" + "\n"
        signature_origin += f"date: {format_date}" + "\n"
        signature_origin += f"POST {path} HTTP/1.1"
        # 进行hmac-sha256加密
        signature_sha = hmac.new(
            self.api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding="utf-8")
        # 构建请求参数
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        # 将请求参数使用base64编码
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
            encoding="utf-8"
        )
        return {
            "host": self.host,
            "date": format_date,
            "authorization": authorization,
        }

    # 创建任务
    def test_create(self, text):
        # 创建任务的路由
        create_path = "/v1/private/dts_create"
        # 拼接鉴权参数后生成的url
        auth_url = self.assemble_auth_url(create_path)
        # 合成文本
        encode_str = base64.encodebytes(text.encode("UTF8"))
        txt = encode_str.decode()
        # 请求头
        headers = {"Content-Type": "application/json"}
        # 请求参数，字段具体含义见官网文档：https://aidocs.xfyun.cn/docs/dts/%E6%8E%A5%E5%8F%A3%E5%8D%8F%E8%AE%AEv3.html
        data = {
            "header": {
                "app_id": self.app_id,
            },
            "parameter": {
                "dts": {
                    "vcn": "x4_guanshan",
                    # [x4_pengfei x4_yeting x4_qianxue x4_guanshan x4_lingxiaoqi_assist x4_lingfeihong_document_n]
                    "language": "zh",
                    "speed": 50,
                    "volume": 50,
                    "pitch": 50,
                    "rhy": 1,
                    "audio": {
                        "encoding": "lame",  # 下方下载的文件后缀需要保持一致
                        "sample_rate": 16000,
                    },
                    "pybuf": {"encoding": "utf8", "compress": "raw", "format": "plain"},
                }
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "text": txt,
                }
            },
        }
        try:
            print("创建任务请求参数:", json.dumps(data))
            res = requests.post(url=auth_url, headers=headers, data=json.dumps(data))
            res = json.loads(res.text)
            return res
        except Exception as e:
            print(f"创建任务接口调用异常，错误详情:{e}")
            sys.exit(1)

    # 查询任务
    def test_query(self, task_id):
        # 查询任务的路由
        query_path = "/v1/private/dts_query"
        # 拼接鉴权参数后生成的url
        auth_url = self.assemble_auth_url(query_path)
        # 请求头
        headers = {"Content-Type": "application/json"}
        # 请求参数，字段具体含义见官网文档：https://aidocs.xfyun.cn/docs/dts/%E6%8E%A5%E5%8F%A3%E5%8D%8F%E8%AE%AEv3.html
        data = {"header": {"app_id": self.app_id, "task_id": task_id}}
        try:
            print("\n查询任务请求参数:", json.dumps(data))
            res = requests.post(url=auth_url, headers=headers, data=json.dumps(data))
            res = json.loads(res.text)
            return res
        except Exception as e:
            print(f"查询任务接口调用异常，错误详情:{e}")
            sys.exit(1)


# 创建任务
def do_create(text):
    # 调用创建任务接口
    test_task = TestTask()
    create_result = test_task.test_create(text)
    print("create_response:", json.dumps(create_result))
    # 创建任务接口返回状态码
    code = create_result.get("header", {}).get("code")
    # 状态码为0，创建任务成功，打印task_id, 用于后续查询任务
    if code == 0:
        task_id = create_result.get("header", {}).get("task_id")
        print(f"创建任务成功，task_id: {task_id}")
        return task_id
    else:
        print(f"创建任务失败，返回状态码: {code}")


# 查询任务
def do_query(task_id):
    test_task = TestTask()
    # 这里循环调用查询结果，当task_status状态为'5'（即大文本合成任务完成）时停止循环，循环次数和sleep时间可酌情定义
    for i in range(9):
        # 等待1秒
        time.sleep(1)
        # 调用查询任务接口
        query_result = test_task.test_query(task_id)
        print("query_response:", json.dumps(query_result))
        # 查询任务接口返回状态码
        code = query_result.get("header", {}).get("code")
        # 状态码为0，查询任务成功
        if code == 0:
            # 任务状态码：1-任务创建成功 2-任务派发失败 4-结果处理中 5-结果处理完成
            task_status = query_result.get("header", {}).get("task_status")
            if task_status == "5":
                audio = query_result.get("payload", {}).get("audio").get("audio")
                # base64解码audio，打印下载链接
                decode_audio = base64.b64decode(audio)
                print(f"查询任务成功，音频下载链接: {decode_audio.decode()}")
                return decode_audio
            else:
                print(f"第{i + 1}次查询，处理未完成，任务状态码:{task_status}")
        else:
            print(f"查询任务失败，返回状态码: {code}")
            sys.exit(1)


if __name__ == "__main__":
    # 1、用户参数，相关参数注意修改
    HOST = "api-dx.xf-yun.com"
    str_list = [
        "2023年，子公司管理部根据公司“正规化、体系化、制度化、专业化”的管理要求，",
        "调整原有的投后管理为主的模式，现阶段对子公司的管理会以财务管控型为主、局部操作型管控为辅。",
        "根据管理需求，选聘管理人员充实子公司经营管理层、建立并完善子公司管理制度、整理母子公司管理流程并稳妥推进优化",
        "开展经营及离任审计并严肃处理有关违规违纪人员，积极跟进整改审计发现的问题；",
        "根据子公司不同业态和发展阶段差异，有侧重点的编制2024年经营计目标，匹配相对应的组织绩效考核体系，为子公司发展步入正轨打下了坚实的基础。",
    ]
    for item in str_list:
        text = item
        task_id = do_create(text)

        # with open("./xjLib/xt_xfspeech/1.txt", encoding="utf-8") as file:
        #     text = file.read()
        #     task_id = do_create(text)
        # 3、执行查询任务
        # 创建任务执行成功后，由返回的task_id执行查询任务
        if task_id:
            query_result = do_query(task_id)

            # 4、下载到本地
            Download_addres = query_result
            f = requests.get(Download_addres)
            # 下载文件，根据需要更改文件后缀
            filename = "tts.mp3"
            with open(filename, "wb") as code:
                code.write(f.content)
            if filename:
                print("\n音频保存成功！")
            else:
                print("\n音频保存失败！")

        ##半成品，待完善
