#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys
sys.path.append(sys.path[0].replace("/bin",""))
from util import RedisFunc

r = RedisFunc.getInstance()
# r.public('{"updateInfo":{"projectName":"JERSEYBBW","projectVersion":"v8"}}')
# r.public('{"method":"updateProject","projectName":"JERSEYBBW","projectVersion":"v8"}')
# r.public('{"method":"updateProject","projectName":"INSHACCDEMO","projectVersion":"v1"}')
# r.public('{"method":"restartProjectTom","projectName":"INSHACCDEMO"}')
# r.public('{"method":"stopOneTomcat","tomcatId":"46"}')
# r.public('{"method":"startOneTomcat","tomcatId":"46"}')
r.public('{"method":"restartOneTomcat","tomcatId":"46"}')
# r.public('{"method":"startTomcat","tomcatId":"46"}')
# r.public('{"method":"localUpdateProject","projectName":"INSHACCDEMO","projectVersion":"v1"}')


