#!/usr/bin/env python
# encoding: utf-8

import jmo_sap_rfc as a
conn=a.main('formal')
i=1
with open('bomlist.txt','r') as src:
    with open('result.txt','w') as dest:
        for line in src:
            print i
            i=i+1
            line=line.rstrip('\r\n')
            result=conn.isBomExist(material_code=line)
            conn.conn.close()
            dest.write('%s %s\n' % (line,result))

