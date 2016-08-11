#!/usr/bin/env python
# encoding: utf-8

import jmo_sap_rfc
sapconn=jmo_sap_rfc.main('Hformal')
i=0
with open('./towrite/spe.txt','r') as src:
    with open('result.txt','w') as dest:
        for line in src:
            i=i+1
            print i
            line=line.rstrip('\r\n')
            res=sapconn.write_bom(pcode=line)
            resul=res['T_RETURN'][0]['MSG']
            resul=resul.encode('utf-8')
            sapconn.conn.close()
            dest.write('%s %s\n' % (line,resul))

