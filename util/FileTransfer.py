import paramiko
from util import PrintLog
from bin import WorkThread
import time
LogObj = PrintLog.getInstance()


class FileTransfer:
    def __init__(self, hostname, username, password, port=22):
        self.ssh = paramiko.SSHClient()  # 创建SSH对象
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        self.ssh.connect(hostname=hostname, port=port, username=username, password=password)  # 连接服务器

    # 获取远程服务器文件到本地
    def getFile(self, remoteFile, localFile):
        self.ssh.open_sftp().get(remoteFile, localFile)

    # 在远程服务器上执行命令
    def exec_command(self, cmd):
        stdin, cmd, stder = self.ssh.exec_command(cmd)
        return cmd

    # 关闭连接
    def close(self):
        self.ssh.close()
        time.sleep(3)


def getInstance( hostname, username, password, port=22):
    return FileTransfer(hostname, username, password, port=port)
