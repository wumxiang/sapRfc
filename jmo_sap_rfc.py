# encoding:utf-8
from pyrfc import Connection
from ConfigParser import ConfigParser
import re
from MssqlODBCConn import MssqlConnection
from datetime import datetime


class main():
    def __init__(self,server='testing'):
        config = ConfigParser()
        config.read('sapnwrfc.cfg')
        params_connection = config._sections[server]
        self.conn = Connection(**params_connection)

    def qry(self, Fields, SQLTable, Where = '', MaxRows=50, FromRow=0):
        """A function to query SAP with RFC_READ_TABLE"""

        # By default, if you send a blank value for fields, you get all of them
        # Therefore, we add a select all option, to better mimic SQL.
        if Fields[0] == '*':
            Fields = ''
        else:
            Fields = [{'FIELDNAME':x} for x in Fields] # Notice the format

        # the WHERE part of the query is called "options"
        options = [{'TEXT': x} for x in Where] # again, notice the format

        # we set a maximum number of rows to return, because it's easy to do and
        # greatly speeds up testing queries.
        rowcount = MaxRows

        # Here is the call to SAP's RFC_READ_TABLE
        tables = self.conn.call("RFC_READ_TABLE", QUERY_TABLE=SQLTable, DELIMITER='|', FIELDS = Fields, OPTIONS=options, ROWCOUNT = MaxRows, ROWSKIPS=FromRow)

        # We split out fields and fields_name to hold the data and the column names
        fields = []
        fields_name = []

        data_fields = tables["DATA"] # pull the data part of the result set
        data_names = tables["FIELDS"] # pull the field name part of the result set

        headers = [x['FIELDNAME'] for x in data_names] # headers extraction
        long_fields = len(data_fields) # data extraction
        long_names = len(data_names) # full headers extraction if you want it

        # now parse the data fields into a list
        for line in range(0, long_fields):
            fields.append(data_fields[line]["WA"].strip())

        # for each line, split the list by the '|' separator
        fields = [x.strip().split('|') for x in fields ]

        # return the 2D list and the headers
        return fields, headers

    def sql_query(self, Query, MaxRows=50, FromRow=0):
        pass
    def create_routing(self, Material='1680001S11PP111', Plant='8000', Sequence=u'管道预制', WorkCenter='JMH1PP02'):
        from datetime import datetime
        op= [{'VALID_FROM': datetime(2015,1,1),
               'VALID_TO_DATE': datetime(9999,12,31),
               'ACTIVITY': '0010',
               'CONTROL_KEY': 'PP01',
               'WORK_CNTR': 'JMH1PP02',
               'PLANT': '8000',
               'STANDARD_TEXT_KEY': '',
               'DESCRIPTION': 'abcdefg',
               'OPERATION_MEASURE_UNIT': 'EA',
               'STD_VALUE_01': '0.000',
               'STD_VALUE_02': '0.000',
               'STD_VALUE_03': '0.000',
               'BASE_QUANTITY': '1.000',
               'MIN_SEND_AHEAD_QTY': '0',
               'MAX_NO_OF_SPLITS': '1',
               'DENOMINATOR': '1',
               'NOMINATOR': '1'}]
        op[0]['WORK_CNTR']=WorkCenter
        op[0]['PLANT']=Plant
        op[0]['DESCRIPTION']=Sequence

        task= [{'GROUP_COUNTER': '01',
                 'VALID_FROM': datetime(2015,1,1),
                 'VALID_TO_DATE': datetime(9999,12,31),
                 'TASK_LIST_USAGE': '1',
                 'PLANT': '8000',
                 'TASK_LIST_STATUS': '4',
                 'TASK_MEASURE_UNIT': 'EA',
                 'LOT_SIZE_TO': '999'}]
        task[0]['PLANT']=Plant

        mta=[{'MATERIAL': '1680001S11PP111',
               'PLANT': '8000',
               'VALID_FROM':  datetime(2015,1,1),
               'VALID_TO_DATE': datetime(9999,12,31)}]
        mta[0]['MATERIAL']=Material
        mta[0]['PLANT']=Plant

        result = self.conn.call("ZPP_ROUTING_CREATE", TASK=task, MATERIALTASKALLOCATION=mta, OPERATION=op)
        print Material,result['O_FLAG']
        return result

    def write_bom(self, pcode='1680001S11PP111',option=0):
        sqlconn=MssqlConnection()
        if option==0:
            res=sqlconn.queryAll(
            """
            SELECT parent_material_code,plant,subsidiary_material_code,sap_code,quantity,unit,material_type,material_desc,type
            FROM production_bom
            WHERE parent_material_code = '%s'
            """%pcode)
        elif option==1:
            res=sqlconn.queryAll(
            """
            WITH RPL (parent_material_code,plant,subsidiary_material_code,sap_code,quantity,unit,material_type,material_desc,type) AS
            (SELECT ROOT.parent_material_code,ROOT.plant,ROOT.subsidiary_material_code,ROOT.sap_code,ROOT.quantity,ROOT.unit,ROOT.material_type,ROOT.material_desc,ROOT.type
            FROM production_bom ROOT
            WHERE ROOT.parent_material_code = '%s'
            Union ALL
            SELECT CHILD.parent_material_code,CHILD.plant,CHILD.subsidiary_material_code,CHILD.sap_code,CHILD.quantity,CHILD.unit,CHILD.material_type,CHILD.material_desc,CHILD    .type
            FROM RPL PARENT, production_bom CHILD
            WHERE Parent.subsidiary_material_code = Child.parent_material_code
            )
            SELECT parent_material_code,plant,subsidiary_material_code,sap_code,quantity,unit,material_type,material_desc
            FROM RPL
            where len(parent_material_code) = 15
            ORDER BY parent_material_code,subsidiary_material_code
            """%pcode)
        else:
             print "请在编码后增加写入方式参数(0为单层写入(缺省)，1为多层写入)"
             return

        item=[]
        elem={}
        #i=0
        #print res
        for row in res:
            #print row
            elem= {'MATNR': row[0],
            'WERKS':  row[1],
            'IDNRK':  row[3],
            'MENGE':  row[4],
            'MEINS':  row[5],
            'STLAN': '1',
            'STLAL': '01',
            'DATUV': datetime(2015,1,2),
            'BMENG': '1',
            'STLST': '01',
            'POSTP': 'L',
            'SANKA': 'X',
            'PREIS': '0.01',
            'SAKTO': '4101010000'}
            item.append(elem)
            #i=i+1
        result = self.conn.call("ZBOM_CREATE_SMP2", T_ITEM=item)
        print result['T_RETURN'][0]['MSG']
        return result

    def isBomExist(self,material_code='1580150C5APP111'):
        fields = ['MATNR']
        table = 'MAST'
        where = ["MATNR = '%s'"%(material_code,)]
        maxrows = 10
        fromrow = 0
        results, headers = self.qry(fields, table, where, maxrows, fromrow)
        #print headers
        #print results
        if results:
            return True
        else:
            return False



if __name__ == '__main__':
    s = main('testing2')
    fields = ['MATNR']
    table = 'MAST'
    where = ["MATNR = '1580150C5APP11'"]
    maxrows = 10
    fromrow = 0
    results, headers = s.qry(fields, table, where, maxrows, fromrow)
    print headers
    print results
