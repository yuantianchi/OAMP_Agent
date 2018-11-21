import os
# 检查tomcat是否启动成功
# def getTomcatPid( tomcatName):
#     execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % tomcatName
#     result = os.popen(execCmd)
#     pidstr = result.read().strip()
#     pidList = pidstr.split("\n")
#     return pidList
# print(getTomcatPid("tomcatA46")[0])
# def checkTomcat( tomcatName):
#     execCmd = "ps -ef|grep %s|grep -v 'grep'|awk '{print $2}'" % tomcatName
#     result = os.popen(execCmd)
#     pidList = result.read()
#     if not str(pidList).strip():
#         return False
#     return True
# import time
# import threading
# class MyTest:
#     def __init__(self, a):
#         self.a=a
#
#     # def test(self):
#     #     self.b=1
#     #     pass
#     def test2(self,b):
#         self.b=b
#         time.sleep(10)
#         pass
#
#     def test3(self):
#         print(self.__class__)
#         print("B:",self)
#
# def getInstance(a):
#     return MyTest(a)
#
# def test4(a,b):
#     T1=getInstance(a)
#     T1.test2(b)
#     T1.test3()
#
#
# if __name__=='__main__':
#         t1=threading.Thread(target=test4,args=(1,5))
#         t2=threading.Thread(target=test4,args=(2,55))
#         t2.start()
#         t1.start()
# class Desc:
#     def __get__(self, ins, cls):
#         print('self in Desc: %s ' % self )
#         # print(self, ins, cls)
# class Test:
#     x = Desc()
#     def prt(self):
#         print('self in Test: %s' % self)
# t = Test()
# t.prt()
# t.x
# def testdef():
#     print(11)
#     exit(1)
# if __name__ == '__main__':
#     try:
#         q=111
#         testdef()
#         p=2
#         print(p)
#     except BaseException as e:
#         print("xxxx",e)

# class MyTest:
#     def __init__(self):
#         pass
#     def test(self):
#         self.b=1
#         print(self)
#
# print(MyTest())
# MyTest().test()
from bin import Init
if __name__ == '__main__':
    s = 'xx '
    if s.strip() == '':
        print ('s is null')
    if s.strip():
        print('s is null2')