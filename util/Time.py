import time
import datetime


class TimeSwitch:

    def datatimeToSeconds(timeStr):
        d = datetime.datetime.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        return time.mktime(d.timetuple())

    def secondsToDatatime(timeStr):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timeStr)))

    def isTime(timeStr):
        try:
            time.strptime(timeStr, "%Y%m%d")
            return True
        except:
            return False

    """
    获取当前时间
    """

    def getCurrentTime(self):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        return nowTime

    """
    获取时间差
    """

    def getReduceTime(self, startTime, endTime):
        nowTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        return (endTime - nowTime).seconds


def getIntance():
    return TimeSwitch()
