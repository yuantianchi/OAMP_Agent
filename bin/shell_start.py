import sys

sys.path.append(sys.path[0].replace("/bin", ""))

import getopt
from util import PrintLog
from bin import Menu

method = None
projectName = None
projectVersion = None

logObj = PrintLog.getInstance()

if __name__ == '__main__':

    options, args = getopt.getopt(sys.argv[1:], "hm:p:v:", ["help", "method=", "project=", "version="])
    if (len(options) <= 0):
        method = "help"
    else:
        for name, value in options:
            if name in ['-h', '--help']:
                if method is not None:
                    logObj.error("请使用正确的方法")
                    sys.exit(1)

            elif name in ['-m', '--method']:
                if value is None or str(value).startswith("-"):
                    logObj.info("-m:--method 需要参数method名")
                    sys.exit(1)
                method = value

            elif name in ['-p', '--project']:
                if value is None or str(value).startswith("-"):
                    logObj.info("-m:--project 需要参数projectname")
                    sys.exit(1)
                projectName = value

            elif name in ['-v', '--version']:
                if value is None or str(value).startswith("-"):
                    logObj.info("-v:--version 需要参数version")
                    sys.exit(1)
                projectVersion = value
            else:
                method = "help"

    info = {"method": method, "projectName": projectName, "projectVersion": projectVersion}
    Me = Menu.getInstance(info)
    if method in Me.getMethods():
        getattr(Me, method)()
    else:
        Me.help()
