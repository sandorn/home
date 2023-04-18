import requests

page = 1
url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
while True:
    data = {
        'cname': '上海',
        'pid': '',
        'pageIndex': page,
        'pageSize': '10'
    }
    response = requests.post(url, data=data)
    print(response.json())

    if response.json().get('Table1', ''):
        page += 1
    else:
        break
