import redis
import time
import threading

from util import JsonFileFunc
from util import Path

jff = JsonFileFunc.getInstance()
p = Path.getInstance()


class RedisFunc:
    def __init__(self):
        self.confPath = p.confDirPath + "conf.json"
        redisConfig = jff.readFile(self.confPath)["proxyRedis"]
        self.ip = redisConfig["serverIP"]
        self.port = redisConfig["port"]
        self.password = redisConfig["password"]
        self.channel = redisConfig["channel"]

        self.__conn = redis.Redis(host=self.ip, port=self.port, password=self.password)

    # 发布
    def public(self, msg):
        self.__conn.publish(self.channel, msg)
        return True

    # 订阅
    def subscribe(self):
        # 打开收音机
        pub = self.__conn.pubsub()
        # 调频道
        pub.subscribe(self.channel)
        # 准备接收
        pub.parse_response()
        return pub


    # 解决长时间不进行操作,服务端可能会断开订阅问题
    def keep_alive(self):
        """
        保持客户端长连接
        """
        ka_thread = threading.Thread(target=self._ping)
        ka_thread.start()

    def _ping(self):
        """
        发个消息，刷存在感
        """
        while True:
            time.sleep(60)
            # 尝试向redis-server发一条消息
            if not self.conn.ping():
                del self._sentinel
                self.__conn = redis.Redis(host="192.168.7.219", port=6379, password="longrise")


def getInstance():
    return RedisFunc()
