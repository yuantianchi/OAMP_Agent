#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys
sys.path.append(sys.path[0].replace("/bin",""))
from util import RedisFunc

r = RedisFunc.getInstance()
# r.public('{"updateInfo":{"projectName":"JERSEYBBW","projectVersion":"v8"}}')
r.public('{"method":"updateProject","projectName":"JERSEYBBW","projectVersion":"v8"}')
# r.public('{"method":"updateProject","projectName":"INSHACCDEMO","projectVersion":"v1"}')
