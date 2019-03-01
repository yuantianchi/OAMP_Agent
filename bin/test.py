import sys
sys.path.append(sys.path[0].replace("/bin", ""))
from bin.base.tool import JsonFileFunc
import requests
from bin.base.tool import Path
J = JsonFileFunc.getInstance()
import time,threading
import os,json
import codecs
from bin.base.log import PrintLog
L=PrintLog.getInstance()


if __name__ == '__main__':
#     path = 'Y:\\project_update_remark_bak\\INSY125\\3\\static'
#     x = os.listdir(path)
#     print(x)

    # r=os.system("\cp -rf /data/smbshare/project_update_share/INSY125/3/static/* /usr/longrise/LEAP/INSY125/WEB-INF/ResourceLib.TMP/INSY125/LEAP/")
    # print(r)
    # 重启某个项目对应的所有tomcat
    # value = {"data":{"method": "restartProject", "projectName": "INSY125"}}
    # r = requests.post('http://192.168.5.110:3099/OAMP_agent/service', data=J.json_to_str(value))
    # print(r.status_code)
    # print(r.content)
    # 项目更新
    # value = {"data": {"method": "updateProject", "projectName": "INSHACCDEMO","projectVersion":"2.1", "opt_id":"123456"}}
    # r = requests.post('http://192.168.7.219:3099/OAMP_agent/service', data=J.json_to_str(value))
    # # r = requests.post('http://127.0.0.1:3099/OAMP_agent/service', data=J.json_to_str(value))
    # print(r.status_code)
    # print(r.content)
    # #获取项目状态
    # value = {"data":{"method": "getProjectStatus", "projectName": "INSHACCDEMO","operateId":"xxxxxxx"}}
    # r = requests.post('http://192.168.7.219:3099/OAMP_agent/service', data=J.json_to_str(value))
    # print(r.status_code)
    # print(r.content)

    # #替换资源
    # value = {"data":{"method": "replaceResource", "projectName": "INSHACCDEMO","projectVersion": "2.1"}}
    # r = requests.post('http://192.168.5.110:3099/OAMP_agent/service', data=J.json_to_str(value))
    # print(r.content)
    #
    # #初始化项目信息

    x = {
        "data": {
            "confData": {
              "INSHACCDEMO": {
                'upstream_conf_file': '/usr/local/nginx/conf/nginx.conf',
                'redis_ip': '192.168.7.219',
                'redis_port': 6379,
                'redis_password': 'longrise',
                'local_ip': '192.168.7.216',
                'backupConfPath': '',
                "projectHome": "/usr/longrise/LEAP/INSY125",
                "projectType": "LEAP",
                "backupFilePath": '/data/smbshare/tmp/1.txt',
                "maxRestartCount": 3,
                "tomcatInfo": [
                    {
                        "port": "8073",
                        "name": "tomcatA72"
                    }
                ],
                "backupConfPath": "",
                "serviceMaxCheckTime": 100,
                "serviceCheckUrl": "/LEAP/Resource/generalIndex/Login2.html",
                "project_name": "OAMP_项目更新测试"
            }
            },
            "method": "initProjectConf"
        }
    }
    r = requests.post('http://192.168.5.110:3099/OAMP_agent/service', data=J.json_to_str(x))
    # #重启某个tomcat
    # value = '{"method": "restartOneTomcat", "projectName": "INSY125","tomcatName":"tomcatA74"}'
    # r = requests.post('http://192.168.5.110:3099', data={"data": value})
    # #关闭某个tomcat
    # value = '{"method": "stopOneTomcat", "projec          tName": "INSY125","tomcatName":"tomcatA74"}'
    # r = requests.post('http://192.168.5.110:3099', data={"data": value})
    # # 开启某个tomcat
    # value = '{"method": "startOneTomcat", "projectName": "INSY125","tomcatName":"tomcatA74"}'
    # r = requests.post('http://192.168.5.110:3099', data={"data": value})

    # class testfile:
    #     def __init__(self):
    #         pass
    #
    #     def write(self):
    #         L.info("进入write")
    #         try:
    #             time.sleep(1)
    #             with codecs.open(path, 'w', encoding='utf-8') as f:
    #                 L.info("write，打开文件")
    #                 time.sleep(4)
    #                 f.write(json.dumps(x, ensure_ascii=False, indent=4))
    #         except Exception as e:
    #             L.error("write [  %s ] not exists, %s", str(path), str(e))
    #         L.info("write结束")
    #
    #     def read(self):
    #         for i in range(10):
    #             data = None
    #             L.info("进入read")
    #             try:
    #                 with open(path, "r", encoding="utf-8") as f:
    #                     L.info("read，打开文件")
    #                     data = json.load(f)
    #                     time.sleep(2)
    #             except Exception as e:
    #                 L.error("read [  %s ] not exists, %s", str(path), str(e))
    #             L.info("read结束")
    #             L.info(data)
    #         time.sleep(1)
#     P = Path.getInstance()
#     path = P.confDirPath + os.sep + "info.json"
#
#     x = {
#         "data": {
#             "confData": {
#                 "BBT": {
#                     "projectType": "LEAP",
#                     "serviceMaxCheckTime": 600,
#                     "tomcatInfo": [{"name": "tomcatA02", "port": "8002"},
#                                    {"name": "tomcatA03", "port": "8003"},
#                                    {"name": "tomcatA04", "port": "8004"},
#                                    {"name": "tomcatA01", "port": "8001"}],
#                     "backupFilePath": "/datafile/fileshare/DevOps/project_update\\BBT",
#                     "project_name": "保宝app",
#                     "backupConfPath": "",
#                     "maxRestartCount": 3,
#                     "projectHome": "/usr/longrise/LEAP/BBT",
#                     "serviceCheckUrl": "/BBT/restservices/servicecheck/oamp_checkTomcatAvailable/query"
#                 }
#             },
#             "method": "initProjectConf"
#         }
#     }
#
# t2 = threading.Thread(target=testfile().read)
# t1 = threading.Thread(target=testfile().write)
# # t3=threading.Thread(target=testfile().write)
# # t4=threading.Thread(target=testfile().read)
#
#
# t2.start()
# t1.start()
# t1.join()
# t2.join()

# t3.start()
# t4.start()
# class WorkThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         # super(WorkThread, self).__init__()
#
#     def run(self):