# -*- coding: utf-8 -*-
import pyodbc
import ConfigParser

class MssqlConnection:

    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("sapnwrfc.cfg")
        self.host = cf.get("DB","host")
        self.user = cf.get("DB","user")
        self.pwd = cf.get("DB","pwd")
        self.db = cf.get("DB","db")
        conn_info ='DRIVER={FreeTDS};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s;port=1433;TDS_Version=7.0' % (self.db, self.host, self.user, self.pwd)
        self.cnxn=pyodbc.connect(conn_info,unicode_results=True)
        self.cursor=self.cnxn.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
            print(self.cursor,'cursor closed')
        if self.cnxn:
            self.cnxn.close()

    def destroy(self):
        if self.cursor:
            #print(self.cursor,'cursor closed')
            self.cursor.close()
        if self.cnxn:
            self.cnxn.close()

    def queryAll(self,qryStr):
        '''
            获取全部查询结果
        '''
        #print(qryStr)
        self.cursor.execute(qryStr)
        return self.cursor.fetchall()

    def queryField(self,qryStr):
        '''
            获取Field
        '''
        #print(qryStr)
        self.cursor.execute(qryStr)
        return self.cursor.description


    def querySome(self,qryStr,maxcnt):
        '''
            获取前maxcnt条查询结果
        '''
        self.cursor.execute(qryStr)
        return self.cursor.fetchmany(maxcnt)

    def queryPage(self,qryStr,skipCnt,pageSize):
        '''
            获取分页查询结果
        '''
        self.cursor.execute(qryStr)
        self.cursor.skip(skipCnt)
        return self.cursor.fetchmany(pageSize)

    def count(self,qryCntSql):
        '''
            获取查询条数
        '''
        self.cursor.execute(qryCntSql)
        return self.cursor.fetchone()[0]

    def executeDML(self,dmlsql):
        '''
            执行DML语句，包括增删改
        '''
        cnt=self.cursor.execute(dmlsql).rowcount
        self.cnxn.commit()
        return cnt
