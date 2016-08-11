
#!/usr/bin/env python
# encoding: utf-8

# 程序功能
# 1.查询数据库中所有工作令JMH开始的并且sap注册状态为已注册的物料。
# 2.检查1中数据是否在SAP中注册，如果未注册，修改数据库中标识。

import pyodbc
from pyrfc import Connection
import os

#sapConn = Connection(ashost='199.234.20.50', sysnr='00', client='400',
user='handlsx    ', passwd='handhand', pagecode='8400')
sapConn = Connection(ashost='199.234.20.66', sysnr='00', client='800',
user='smp-xm',     passwd='gcxmgy11', pagecode='8400')
sqlCnxn =
pyodbc.connect('DRIVER={FreeTDS};SERVER=199.234.20.71;PORT=1433;DATABASE=SM
PPlatform;UID=smpplatform;PWD=ZzS)m@TkTX')
sqlCursor = sqlCnxn.cursor()

sqlData=sqlCursor.execute(
"""
