#!/usr/bin/env python
# encoding: utf-8
from MssqlODBCConn import MssqlConnection
desc = "99-10-PL-23232-A1E-H(50)-1"
conn=MssqlConnection()
res=conn.queryAll(
    """
    select subsidiary_material_code,material_desc
    from production_bom where material_desc like '%s'
    """ % desc
)
conn.destroy()
print res
#i=0
#with open('./towrite/spe.txt','r') as src:
#    with open('result.txt','w') as dest:
#        for line in src:
#            i=i+1
#            print i
#            line=line.rstrip('\r\n')
#            res=sapconn.write_bom(pcode=line)
#            resul=res['T_RETURN'][0]['MSG']
#            resul=resul.encode('utf-8')
#            sapconn.conn.close()
#            dest.write('%s %s\n' % (line,resul))
#
