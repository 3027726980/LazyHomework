import json
from pathlib import Path

from Naked.toolshed.benchmarking import timer

from function import myLog,checkFolder

# 显示所有课程
def showAllCourse():
    if checkFolder("Data/CourseList") == 0:
        courseFolder = list(Path("Data/CourseList").glob("*.json"))
        # 遍历文件夹
        for i in courseFolder:
            with open(i, "r", encoding="utf-8") as f:
                # 暂时存放读取的文件数据
                fileData = f.read()
                CourseName = json.loads(fileData).get("name")
                teacherName = json.loads(fileData).get("teacherName")
                print(f"课程名称:\t{CourseName}")
                print(f"教师名称:\t{teacherName}\n")
        print(f"课程总计: {len(courseFolder)}\n")
        myLog("showAllCourse Success")
        return 0
    else:
        myLog("Course Folder Not Exists")
        return 7

# 显示所有待完成的作业
def showUnHomework():
    totalUnHomework = 0
    courseUnHomeWork = 0
    unHomeworkCourse = 0
    if checkFolder("Data/HomeworkList") == 0:
        homeworkFolder= list(Path("Data/HomeworkList").glob("*.json"))
        # 遍历文件夹
        for i in homeworkFolder:
            with open(i, "r", encoding="utf-8") as f:
                homeworkList = json.loads(f.read())

            # 遍历作业列表统计该课程的待完成作业
            for j in homeworkList:
                status = j.get("status")
                if status == 2:
                    # 计数该课程所有待完成的作业
                    courseUnHomeWork += 1

            # 判断该课程是否有待完成的作业
            if courseUnHomeWork != 0:
                # 有待完成作业的课程计数器加1
                unHomeworkCourse += 1
                # 输出课程信息
                with open(f"Data/CourseList/{i.name.split('.')[0]}.json", "r", encoding="utf-8") as f:
                    fileData = f.read()
                    CourseName = json.loads(fileData).get("name")
                    teacherName = json.loads(fileData).get("teacherName")
                    print(
                        "---------------------------------------------------------------------------------------------------")
                    print(f"课程名称:\t{CourseName}")
                    print(f"教师名称:\t{teacherName}\n")
                    # 输出作业信息
                    for k in homeworkList:
                        status = k.get("status")
                        if status == 2 :
                            # 计数所有待完成的作业
                            totalUnHomework += 1
                            homeworkTitle = k.get("homeworkTitle")
                            print(f"作业标题:\t{homeworkTitle}")
                            print(f"时间状态:\t未截至")
                            print(f"作业状态:\t未完成\n")
                    print(f"该课程待完成作业总计: {courseUnHomeWork}")
                    print("---------------------------------------------------------------------------------------------------\n")
                    # 重置该课程待完成作业计数器
                    courseUnHomeWork = 0
            else:
                # 输出日志
                myLog(f"{i.name.split('.')[0]} No UnHomework")
        print(f"待完成作业总计: {totalUnHomework}")
        print(f"课程总计: {unHomeworkCourse}\n")
        # 输出日志
        myLog(f"showUnHomework Finished: \n need to do homework total {totalUnHomework}\n from {unHomeworkCourse} course")

if __name__ == "__main__":
    showUnHomework()