import http.client, requests
import json

from requests.exceptions import ConnectionError, Timeout
from function import myLog,checkFolder
from save import save
from pathlib import Path

# 初始化参数
conn = http.client.HTTPSConnection('courseapi.ulearning.cn')

# 检查账号密码是否正确
def checkLoginData(loginName, password):
    print("Checking LoginData...")
    # 定义请求参数登录名和密码
    params = {
        'loginName': loginName,
        'password': password,
    }

    try:
        # 发送GET请求，包含参数和设置超时时间为20秒
        response = requests.get('https://courseapi.ulearning.cn/users/check', params=params, timeout=20)
        # 处理返回响应的JSON数据判断登录是否成功
        if response.json()['result'] == 0:
            # 打印账号密码错误日志
            myLog(f'LoginName or Password is wrong')
            # 打印账号密码错误日志并返回错误代码
            return 1
        elif response.json()['result'] == 1:
            # 打印账号密码正确日志并返回True
            myLog(f'LoginData is right')
            return 0
        elif response.json()['result'] == 3:
            # 打印账号密码错误太多次错误日志并返回错误代码
            myLog(f'Mistake too much')
            return 2
    except ConnectionError:
        # 发生连接错误时打印错误信息并返回错误代码
        myLog(f'ConnectionError: Please check network')
        return 3
    except Timeout:
        # 请求超时时打印错误信息
        myLog(f'ConnectionError: Spend too much time')
        return 4
    except Exception as e:
        # 发生其他错误时打印错误信息并返回错误代码
        myLog(f'Error: {e}')
        return 5

# 登录获取Token以及USERINFO
def login(loginName, password):
    print("Login...")
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://umooc.ulearning.cn',
        'Referer': 'https://umooc.ulearning.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    result = {}
    conn.request('POST', '/users/login/v2', f'loginName={loginName}&password={password}', headers)
    response = conn.getresponse()
    # 打印返回头信息日志
    myLog(f"{response.headers}")
    # 获取返回头信息中设置的token和userinfo
    for i in response.headers.values():
        if ("AUTHORIZATION" in i) or ("token" in i):
            result["token"] = i.split(";")[0].split("=")[-1]
            # 打印获取token日志
            myLog(f"Get token :{result.get('token')}")
        if "USERINFO" in i:
            result["userinfo"] = i.split(";")[0].split("=")[-1]
            # 打印获取userinfo日志
            myLog(f"Get token :{result.get('userinfo')}")
    # 打印返回结果日志
    myLog(f"result:{result}")
    return result

# 获取课程列表
def getCourseList(token):
    print("Get CourseList...")
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://courseweb.ulearning.cn',
        'Referer': 'https://courseweb.ulearning.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'keyword': '',
        'publishStatus': '1',
        'type': '1',
        'pn': 1,
        'ps': 1,
        'lang': 'zh',
    }

    try:
        # 发送GET请求，包含参数和设置超时时间为20秒
        response = requests.get('https://courseapi.ulearning.cn/courses/students', headers=headers, params=params, timeout=20)
    except ConnectionError:
        # 发生连接错误时打印错误信息并返回错误代码
        myLog(f'ConnectionError: Please check network')
        return 3
    except Timeout:
        # 请求超时时打印错误信息
        myLog(f'ConnectionError: Spend too much time')
        return 4
    except Exception as e:
        # 发生其他错误时打印错误信息并返回错误代码
        myLog(f'Error: {e}')
        return 5
    else:
        if response.json().get("total") != params.get("ps") and response.json().get("total") != 0:
            params["ps"] = response.json().get("total")
            response = requests.get('https://courseapi.ulearning.cn/courses/students', headers=headers, params=params)
            # 打印获取课程列表成功日志
            myLog(f"Get CourseList Successfully: \n{response.json()}")
            # 遍历课程列表并储存到CourseList文件夹
            for i in response.json().get("courseList"):
                save(json.dumps(i, ensure_ascii=False, indent=4), "CourseList", "json",f'{i.get("id")}')
        else:
            # 打印获取课程列表成功日志
            myLog(f"Get CourseList Successfully: \n{response.json()}")
            # 遍历课程列表并储存到CourseList文件夹
            for i in response.json().get("courseList"):
                save(json.dumps(i, ensure_ascii=False, indent=4), "CourseList", "json", f'{i.get("id")}')
        return 0

# 获取作业列表
def getHomeworkList(token):
    print("Get HomeworkList...")
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://courseweb.ulearning.cn',
        'Referer': 'https://courseweb.ulearning.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    courseIDList = []

    checkFolder("Data/CourseList")
    if checkFolder("Data/CourseList") == 0:
        for i in list(Path("Data/CourseList").glob("*.json")):
            with open(i, "r", encoding="utf-8") as f:
                courseIDList.append(json.loads(f.read()).get("id"))

    for i in courseIDList:
        params = {
            'ocId': i,
            'pn': '1',
            'ps': 1,
            'lang': 'zh',
        }

        try:
            # 发送GET请求，包含参数和设置超时时间为20秒
            response = requests.get('https://courseapi.ulearning.cn/homeworks/student/v2', headers=headers, params=params, timeout=20)
        except ConnectionError:
            # 发生连接错误时打印错误信息并返回错误代码
            myLog(f'ConnectionError: Please check network')
            return 3
        except Timeout:
            # 请求超时时打印错误信息
            myLog(f'ConnectionError: Spend too much time')
            return 4
        except Exception as e:
            # 发生其他错误时打印错误信息并返回错误代码
            myLog(f'Error: {e}')
            return 5
        else:
            if response.json().get("total") != params.get("ps") and response.json().get("total") != 0:
                params["ps"] = response.json().get("total")
                response = requests.get('https://courseapi.ulearning.cn/homeworks/student/v2', headers=headers, params=params)
                # 打印获取作业列表成功日志
                myLog(f"Get HomeworkList Successfully: \n{response.json()}")
                # 打印获取作业成功日志
                save(json.dumps(response.json().get("homeworkList"), ensure_ascii=False, indent=4), "HomeworkList", "json", f'{i}')
            elif response.json().get("total") == 0:
                myLog(f"course {i} has no homework")
            else:
                # 打开文件准备写入作业列表数据
                save(json.dumps(response.json().get("homeworkList"), ensure_ascii=False, indent=4), "HomeworkList", "json", f'{i}')
                # 打印获取作业成功日志
                myLog(f"Get HomeworkList Successfully: \n{response.json()}")
