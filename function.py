import time,os,inspect,json
from pathlib import Path

config = json.loads(open('config.json', 'r', encoding='utf-8').read())
errorMsg = config["errorMsg"]

# 日志输出函数
def myLog(message):
    # 获取调用栈中的前一个帧（即调用mylog的那个函数的帧）
    previousFrame = inspect.currentframe().f_back

    # 从帧对象中提取文件名和行号
    filePath = inspect.getframeinfo(previousFrame).filename
    fileName = os.path.basename(filePath)  # 只保留文件名部分

    # 获取调用者的函数名
    funcName = previousFrame.f_code.co_name
    with open('log.txt', 'a+', encoding='utf-8') as f:
        # 添加时间
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        # 打印日志信息，包含文件名、函数名和消息
        f.write(f"---<<<From {fileName}/{funcName}>>>---\n")
        f.write(f"{message}\n")

# 打印错误信息
def printErrorMsg(stateCode):
    if stateCode != 0:
        print("错误码：", stateCode)
        # 打印错误信息
        print(errorMsg.get(str(stateCode)))

# 检查文件夹是否存在
def checkFolder(path):
    if Path(path).exists() and Path(path).is_dir():
        myLog(f"Folder Exists: \n{path}")
        return 0
    else:
        myLog(f"Folder Not Exists: \n{path}")
        return 7