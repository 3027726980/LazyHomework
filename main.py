import json
import time

from network import checkLoginData, login, getCourseList, getHomeworkList
from function import printErrorMsg
from show import showUnHomework,showAllCourse

config = json.loads(open('config.json', 'r', encoding='utf-8').read())
mode = ""

if __name__ == '__main__':
    loginName = input("请输入用户名：")
    password = input("请输入密码：")
    # 检查登录数据
    stateCode = checkLoginData(loginName, password)
    if stateCode == 0:
        print("登录成功")

        # 初始化登录数据
        loginCookies = login(loginName, password)
        token = loginCookies.get("token")
        userinfo = loginCookies.get("userinfo")
        # 获取课程列表
        getCourseList(token)
        # 获取作业列表
        homeworkList = getHomeworkList(token)

        print("加载完毕")

        while mode != "0":
            # 获取模式
            print("0:退出")
            print("1:显示所有课程")
            print("2:显示所有显示未完成的作业")
            mode = input("请输入模式：")
            if mode == "0":
                # 退出
                print("将在5秒后退出")
                time.sleep(5)
                break
            elif mode == "1":
                # 显示所有课程
                showAllCourse()
            elif mode == "2":
                # 显示未完成的作业
                showUnHomework()
            else:
                # 打印错误信息
                print("请输入正确的模式")
    else:
        # 打印错误信息
        printErrorMsg(stateCode)
