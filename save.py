import json,time,pathlib

from function import myLog

# 检查路径文件IO是否正常
def checkIO(path):
    # 检查IO错误
    try:
        f = open(path, "w+", encoding="utf-8")
    except IOError:
        # IO错误日志
        myLog(f"IOError:{path}")
        return 7
    except Exception as e:
        # 发生其他错误时打印错误信息并返回错误代码
        myLog(f"UndefinedError: {e}")
        return 5
    else:
        f.close()
        # 输出日志
        myLog(f"IO Successfully:{path}")
        return 0

#以特定格式保存数据到指定路径
def save(data, path, format = "txt",name = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"):
    # 获取当前脚本所在的目录
    projectRoot = pathlib.Path(__file__).parent
    # 定义目标文件夹
    targetFolder = projectRoot/"Data"/ path
    # 创建目标文件夹，如果它不存在
    targetFolder.mkdir(parents=True, exist_ok=True)

    # 创建文件路径
    path = f"{targetFolder}/{name}.{format}"
    if format == "txt":
        # 检查IO
        if checkIO(path) == 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
        # 输出日志
        myLog(f"Save Successfully: \n{path}")
        return 0
    elif format == "json":
        # 检查json格式
        try:
            json.loads(data)
        except ValueError as e:
            # 输出日志
            myLog(f"Formate Error: \njson format is wrong")
            return 6
        except Exception as e:
            # 发生其他错误时打印错误信息并返回错误代码
            myLog(f"UndefinedError: {e}")
            return 5
        else:
            # 检查IO
            if checkIO(path) == 0:
                with open(path,"w",encoding="utf-8") as f:
                    f.write(data)
                # 输出日志
                myLog(f"Save Successfully: \n{path}")
            return 0
    else:
        myLog(f"Save Failed: {format} is not support")
        return 8
