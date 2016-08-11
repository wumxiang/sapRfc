#!/usr/bin/env python
# encoding: utf-8

import jmo_sap_rfc as a
conn=a.main('Hformal')
i=1
with open('./towrite/spo.txt','r') as src:
    with open('result.txt','w') as dest:
        for line in src:
            print i
            i=i+1
            line=line.rstrip('\r\n')
            result=conn.create_routing(Material=line,
            Plant='8000',Sequence=u'管道安装',WorkCenter='JMH1PP02')
            conn.conn.close()
            dest.write('%s %s\n' % (line,result['O_FLAG']))

