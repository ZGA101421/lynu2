import random
import time
import requests
import re
import json

msg = ""
config={
        "users": [
        # 多个用户复制粘贴用,隔开例如
        # # {
        #     "username": "学号",
        #     "password": "密码"
        #     },{
        #     "username": "学号",
        #     "password": "密码"
        #     }

        {
            "username": "学号",
            "password": "密码"
            }

    ]}
    # www.pushplus.plus
pushplusToken="自己的token去www.pushplus.plus申请"


def UserAgent():  # 随机获取请求头
    # UserAgent = 'Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2785 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/3473 MicroMessenger/8.0.1.1841(0x28000151) Process/appbrand0 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android'
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    UserAgent = random.choice(user_agent_list)
    return UserAgent


def getJWT(username, password):
    login_url = "https://apii.lynu.edu.cn/v1/accounts/login/"
    user = {
        "username": username,
        "password": password,
        "type": ""}
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    s.proxies = {"https": "47.100.104.247:8080", "http": "36.248.10.47:8080", }  # 使用代理
    JWT = request_jwt(login_url, user)
    # print(JWT)
    if 'details' in str(JWT):
        return "dead"
    # print(JWT)
    else:
        JW = "JWT " + JWT["token"]
        # print(JW)
        return JW


# list 转成Json格式数据
def listToJson(lst):
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    # str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return list_json


def request_jwt(url, json):
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip,deflate,br",
        "User-Agent": UserAgent(),
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx93cafd9ca4061c71/27/page-frame.html",
        "Connection": "close",
        "Host": "apii.lynu.edu.cn"}
    r = requests.post(url, headers=headers, json=json)
    return r.json()


def request_lynu(url, json, JWT):
    headers = {
        "Accept-Encoding": "gzip,deflate,br",
        "User-Agent": UserAgent(),
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx93cafd9ca4061c71/27/page-frame.html",
        "Authorization": JWT,
        "Connection": "close",
        "Host": "apii.lynu.edu.cn"}
    r = requests.post(url, headers=headers, json=json)
    return r.json()


def get_location(url, JWT):
    headers = {
        "Accept-Encoding": "gzip,deflate,br",
        "User-Agent": UserAgent(),
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx93cafd9ca4061c71/27/page-frame.html",
        "Authorization": JWT,
        "Connection": "close",
        "Host": "apii.lynu.edu.cn"}
    r = requests.get(url, headers=headers)
    return r.json()


# 随机体温
def sjtw():
    return str(random.randint(362, 369) / 10)


def getTime():
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str(otherStyleTime).split(' ')[0].split('-')[-1]


def start(a, b):
    fail = []
    # 推送配置
    ms = " 姓 &emsp;名|地 &emsp;&emsp;&emsp; &emsp;&emsp;&emsp;址|中高风险地区|健康码颜色|接种情况\n:-|:-|:-|:-|:-\n"
    high_risk_status_list = {"A": "从未去过中高风险地区",
                             "B": "去过中高风险地区，但已返回洛阳",
                             "C": "目前仍在中高风险地区"}
    colors = {"A": "green",
              "B": "yellow",
              "C": "red"}
    global msg
        # config = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', f.read()))
    for user in config['users']:
            password = user['password']
            username = user['username']
            print(username)
            print(password)
            morning_url = "https://apii.lynu.edu.cn/v1/temperatures/"
            noon_url = "https://apii.lynu.edu.cn/v1/noons/"
            jwt = getJWT(username, password)
            if ('dead' in jwt):
                # 密码错误
                continue
            # 获取最新历史数据
            history = get_location(morning_url, jwt)
            user_msg = history["list"][0]
            name = user_msg["reporter_detail"]["name"]
            # print(user_msg)
            address_list = user_msg["location"]
            # 提交表单数据
            # code_color   A 绿色  B 黄色   c 红色
            # vaccine_status A 两针  B 一针 C  因禁忌未接种 D 近期接种 E 不考虑接种
            '''从未去过中高风险地区
                去过中高风险地区，但已返回洛阳
                目前仍在中高风险地区'''

            code_color = user_msg["code_color"]
            timed = str(user_msg['modified']).split(' ')[0].split("-")[-1]

            condition = user_msg['condition']
            home_condition = user_msg['home_condition']
            vaccine_status = user_msg["vaccine_status"]
            high_risk_status = user_msg["high_risk_status"]
            code_color_display = colors[code_color]
            vaccine_status_display = user_msg["get_vaccine_status_display"]
            print("健康码颜色\t\t\t" + code_color_display)
            print("疫苗接种情况\t\t\t" + vaccine_status_display)
            print("16天内中高风险地区\t" + high_risk_status_list[high_risk_status])
            morning_json = {"value": sjtw(),
                            "condition": condition,
                            "code_color": code_color,
                            "vaccine_status": vaccine_status,
                            "home_condition": home_condition,
                            'high_risk_status': high_risk_status,
                            "location":
                                {
                                    "status": 0,
                                    "lat": 34.61,
                                    "lng": 112.46,
                                    "nation": "中国",
                                    "nation_code": "156",
                                    "address": address_list["address"],
                                    "famous": address_list["town_detail"]["fullname"],
                                    "recommend": address_list["recommend"],
                                    "district_code": address_list["town_detail"]['district'],
                                    "district_name": address_list["town_detail"]['name'],
                                    "district_lat": 34.5154,
                                    "district_lng": 112.37,
                                    "town_code": address_list["town_detail"]['id'],
                                    "town_name": address_list["town_detail"]['name'],
                                    "town_lat": 34.62,
                                    "town_lng": 112.44}
                            }
            noon_json = {"value": sjtw(), "condition": condition}
            s = user_msg
            # 已打卡
            if timed == getTime():
                continue
            try:
                s = request_lynu(morning_url, morning_json, jwt)
                time.sleep(2)
                t = request_lynu(noon_url, noon_json, jwt)
            except:
                list.append(fail, name)
            sj = s["created"]
            morning_temperature = s["value"]
            # noon_temperature = t["value"]
            s_name = s["reporter_detail"]["name"]
            s_address = s["location"]["district_detail"]["fullname"]
            print(s_name)
            print(s_address)
            # pushplus 图推送信息配置
            msg += s_name + "|" + s_address + "|" + high_risk_status_list[high_risk_status] + "|" \
                   + "<font style=\"background: " + code_color_display + "\">  ☆☆☆☆☆|" \
                   + vaccine_status_display + "\n"
            # print(msg)

    pushplus(ms, msg)
def pushplus(ms, msg):
    api = "http://www.pushplus.plus/send"
    header = {
        "Content-Type": "application/json"
    }
    title = u"洛师小筑打卡"
    # http://www.pushplus.plus
    ms += msg
    data = {
        "token": pushplusToken,
        "title": title,
        "content": ms,
        "template": "markdown"
    }
    req = requests.post(api, data=data)
    print(req.json())


def main(a, b):
    start(a, b)


def main_handler(event, context):
    start(event,context)
# 使用云函数可以取消注释
if __name__ == '__main__':
    start(1, 2)
