import base64
import json
import os
import random
import requests


def dk(USERNAME, PASSWORD, LOCATION, COORD,token):
    # 小北学生 账号密码
    # USERNAME = '15675842897'
    # PASSWORD = '19990911Zyp'
    # # 经纬度
    # LOCATION = '112.909625,28.35685'
    # # 位置
    # COORD = '中国-湖南省-长沙市-望城区'
    # 基本链接
    PASSWORD = str(base64.b64encode(PASSWORD.encode()).decode())
    BASE_URL = "https://xiaobei.yinghuaonline.com/xiaobei-api/"
    # header
    HEADERS = {
        "user-agent": "iPhone10,3(iOS/14.4) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436",
        "accept": "*/*",
        "accept-language": "zh-cn",
        "accept-encoding": "gzip, deflate, br"
    }

    def get_param():
        # 体温随机为35.7~36.7
        temperature = str(random.randint(357, 367) / 10)
        # 107.807008,26.245838
        rand = random.randint(1111, 9999)
        # 经度
        location_x = LOCATION.split(',')[0].split('.')[0] + '.' + LOCATION.split(',')[0].split('.')[1][0:2] + str(rand)
        # 纬度
        location_y = LOCATION.split(',')[1].split('.')[0] + '.' + LOCATION.split(',')[1].split('.')[1][0:2] + str(rand)
        location = location_x + ',' + location_y
        print(location)
        return {
            "temperature": temperature,
            "coordinates": COORD,
            "location": location,
            "healthState": "1",
            "dangerousRegion": "2",
            "dangerousRegionRemark": "",
            "contactSituation": "2",
            "goOut": "1",
            "goOutRemark": "",
            "remark": "无",
            "familySituation": "1"
        }

    def send_mail(context):
        # SCT159120TbWKSrIW4kF8qkUfuul9JJsMO
        url = "https://sctapi.ftqq.com/"+token+".send"
        js = {'title': context, 'info': context, "desp": context}
        # {"code":200,"msg":"\u606d\u559c\u60a8\u53d1\u9001\u6210\u529f\u4e86"}
        result = requests.post(url, js).text
        print(result)
        type = json.loads(result)['code']
        if type == 0:
            print("通知发送成功！")
        else:
            print("通知发送失败!")

    # Url
    # 滑动验证
    captcha = 'https://xiaobei.yinghuaonline.com/xiaobei-api/captchaImage'
    # 登录
    login = BASE_URL + 'login'
    # 打卡
    health = BASE_URL + 'student/health'
    # post method return 500 , So use the get method
    # data:   {"msg":"操作成功","img":"xxxxxx","code":200,"showCode":"NM6B","uuid":"4f72776b789b44d796722037ba7a1ff0"}
    response = requests.get(url=captcha, headers=HEADERS).text
    # 取得uuid及showCode
    print(response)
    uuid = json.loads(response)['uuid']
    showCode = json.loads(response, strict=False)['showCode']
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "code": showCode,
        "uuid": uuid
    }
    print(data)
    # 登录测试
    # success return {"msg":"操作成功","code":200,"token":"eyJhb....."}
    # error return {"msg":"用户不存在/密码错误","code":500}
    res = requests.post(url=login, headers=HEADERS, json=data).text
    print(res)
    code = json.loads(res)['code']
    msg = json.loads(res)['msg']
    IS_EMAIL = 1
    if code != 200:
        print("Sorry! Login failed! Error：" + msg)
        # 发送邮件
        if IS_EMAIL == 1:
            send_mail("登录失败，失败原因：" + msg)
        return False
    else:
        print("登录成功！")
        # HEADERS.update({'authorization', token})
        # 换个方法
        HEADERS['authorization'] = json.loads(res)['token']
        health_param = None
        if LOCATION is not None and COORD is not None:
            health_param = get_param()
        else:
            print("必要参数为空！")
        respond = requests.post(url=health, headers=HEADERS, json=health_param).text
        # error return {'msg': None, 'code': 500}
        # succeed return {'msg': '操作成功', 'code': 200}
        status = json.loads(respond)['code']
        if status == 200:
            print("恭喜您打卡成功了！")
            if IS_EMAIL == 1:
                send_mail("恭喜您今天打卡成功啦^_^")
        else:
            print("Error：" + json.loads(respond)['msg'])
            if token != '':
                send_mail("Error：" + json.loads(respond)['msg'])
        return True
