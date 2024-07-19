# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-11-08 09:18:15
LastEditTime : 2024-07-18 11:35:25
FilePath     : /CODE/xjLib/xt_xfspeech/cfg.py
Github       : https://github.com/sandorn/home
==============================================================
APPID = 2269c784
APISecret = OWI0NGJmYmQxZTA1OTI1Yjg5MTM4OGUy
APIKey = 5206d42c6146ead1ee5411b106965114
SDK调用方式只需APPID。APIKey或APISecret适用于WebAPI调用方式。
https://console.xfyun.cn/services/tts
在线语音合成(流式版)API:"wss://tts-api.xfyun.cn/v2/tts"
"""

APPID = "2269c784"
APISecret = "OWI0NGJmYmQxZTA1OTI1Yjg5MTM4OGUy"
APIKey = "5206d42c6146ead1ee5411b106965114"

"""
业务参数说明(business)

参数名	类型	必传	描述	示例
aue	string	是	音频编码,可选值:
			raw(默认值):未压缩的pcm	"speex-org-wb;7" 数字代表指定压缩等级(默认等级为8),数字必传
			lame:mp3 (当aue=lame时需传参sfl=1)	标准开源speex编码以及讯飞定制speex说明请参考音频格式说明
			speex-org-wb;7: 标准开源speex(for speex_wideband,即16k)数字代表指定压缩等级(默认等级为8)
			speex-org-nb;7: 标准开源speex(for speex_narrowband,即8k)数字代表指定压缩等级(默认等级为8)
			speex;7:压缩格式,压缩等级1~10,默认为7(8k讯飞定制speex)
			speex-wb;7:压缩格式,压缩等级1~10,默认为7(16k讯飞定制speex)


sfl	int	否	需要配合aue=lame使用,开启流式返回
			mp3格式音频
			取值:1 开启(默认值)
auf	string	否	音频采样率,可选值:	"audio/L16;rate=16000"
			audio/L16;rate=8000:合成8K 的音频
			(默认值)audio/L16;rate=16000:合成16K 的音频
vcn	string	是	发音人,可选值:请到控制台添加试用或购买发音人,添加后即显示发音人参数值	"xiaoyan"
speed	int	否	语速,可选值:[0-100],默认为50
volume	int	否	音量,可选值:[0-100],默认为50
pitch	int	否	音高,可选值:[0-100],默认为50
bgs	int	否	合成音频的背景音	0
			0:无背景音(默认值)
			1:有背景音
tte	string	否	文本编码格式
			GB2312
			GBK
			BIG5
			UNICODE(小语种必须使用UNICODE编码,合成的文本需使用utf16小端的编码方式,详见java示例demo)
			GB18030
			UTF8(默认值)
reg	string	否	设置英文发音方式:
			0:自动判断处理,如果不确定将按照英文词语拼写处理(缺省)
			1:所有英文按字母发音
			2(默认值):自动判断处理,如果不确定将按照字母朗读
rdn	string	否	合成音频数字发音方式
			0:自动判断(默认值)
			1:完全数值
			2:完全字符串
			3:字符串优先
"""
