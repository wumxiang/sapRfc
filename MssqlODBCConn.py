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
            ��ȡȫ����ѯ���
        '''
        #print(qryStr)
        self.cursor.execute(qryStr)
        return self.cursor.fetchall()

    def queryField(self,qryStr):
        '''
            ��ȡField
        '''
        #print(qryStr)
        self.cursor.execute(qryStr)
        return self.cursor.description


    def querySome(self,qryStr,maxcnt):
        '''
            ��ȡǰmaxcnt����ѯ���
        '''
        self.cursor.execute(qryStr)
        return self.cursor.fetchmany(maxcnt)

    def queryPage(self,qryStr,skipCnt,pageSize):
        '''
            ��ȡ��ҳ��ѯ���
        '''
        self.cursor.execute(qryStr)
        self.cursor.skip(skipCnt)
        return self.cursor.fetchmany(pageSize)

    def count(self,qryCntSql):
        '''
            ��ȡ��ѯ����
        '''
        self.cursor.execute(qryCntSql)
        return self.cursor.fetchone()[0]

    def executeDML(self,dmlsql):
        '''
            ִ��DML��䣬������ɾ��
        '''
        cnt=self.cursor.execute(dmlsql).rowcount
        self.cnxn.commit()
        return cnt
