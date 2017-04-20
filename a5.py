from easysnmp import Session
import time, sys
import rrdtool, tempfile

def a5():
    session1 = Session(hostname='10.40.40.194', community='public', version=2)
    session2 = Session(hostname='10.40.40.198', community='public', version=2)

    number1=session1.get('ifNumber.0')
    number2=session2.get('ifNumber.0')

    in_tot_s=0
    out_tot_s=0
    temp1_s=0
    temp2_s=0
    temp3_s=0
    temp4_s=0

    in_tot_r=0
    out_tot_r=0
    temp1_r=0
    temp2_r=0
    temp3_r=0
    temp4_r=0

    inUpac_s=session1.get_bulk("ifInUcastPkts", 0, int(number1.value))
    for i in inUpac_s:
        temp1_s=temp1_s+int(i.value)

    inNUpac_s=session1.get_bulk("ifInNUcastPkts", 0, int(number1.value))
    for i in inNUpac_s:
        temp2_s=temp2_s+int(i.value)

    outUpac_s=session1.get_bulk("ifOutUcastPkts", 0, int(number1.value))
    for i in outUpac_s:
        temp3_s=temp3_s+int(i.value)

    outNUpac_s=session1.get_bulk("ifOutNUcastPkts", 0, int(number1.value))
    for i in outNUpac_s:
        temp4_s=temp4_s+int(i.value)

    inUpac_r=session2.get_bulk("ifInUcastPkts", 0, int(number2.value))
    for i in inUpac_r:
        temp1_r=temp1_r+int(i.value)

    inNUpac_r=session2.get_bulk("ifInNUcastPkts", 0, int(number2.value))
    for i in inNUpac_r:
        temp2_r=temp2_r+int(i.value)

    outUpac_r=session2.get_bulk("ifOutUcastPkts", 0, int(number2.value))
    for i in outUpac_r:
        temp3_r=temp3_r+int(i.value)

    outNUpac_r=session2.get_bulk("ifOutNUcastPkts", 0, int(number2.value))
    for i in outNUpac_r:
        temp4_r=temp4_r+int(i.value)

    in_tot_s=temp1_s+temp2_s
    out_tot_s=temp3_s+temp4_s
    in_tot_r=temp1_r+temp2_r
    out_tot_r=temp3_r+temp4_r


    rrdtool.update('/var/www/html/mrtg/switch.rrd', 'N:%d:%d' %(in_tot_s, out_tot_s))
    rrdtool.update('/var/www/html/mrtg/router.rrd', 'N:%d:%d' %(in_tot_r, out_tot_r))
    FILE1='/var/www/html/mrtg/switch.rrd'
    FILE2='/var/www/html/mrtg/router.rrd'

    fd,path = tempfile.mkstemp('.png')
    info = rrdtool.info(FILE1)
    st=int(info['last_update']-340)
    en=int(info['last_update'])
    rrdtool.graph("/var/www/html/mrtg/switch.png", "-s %d" %st, "-e %d" %en,"--x-grid=MINUTE:1:HOUR:1:MINUTE:1:0:%X", '--watermark=Time' ,"-w 600","-h 350","--vertical-label=Packet Rate", "-t Switch traffic: Past 5 minutes", "DEF:s_in=/var/www/html/mrtg/switch.rrd:in:AVERAGE", "DEF:s_out=/var/www/html/mrtg/switch.rrd:out:AVERAGE", "LINE1:s_in#0000FF:Packets In\r", "LINE2:s_out#00FF00:Packets Out\r")
    
    rrdtool.graph("/var/www/html/mrtg/router.png", "-s %d" %st, "-e %d" %en,"--x-grid=MINUTE:1:HOUR:1:MINUTE:1:0:%X",'--watermark=Time', "-w 600", "-h 350","--vertical-label=Packet Rate", "-t Router traffic: Past 5 minutes", "DEF:r_in=/var/www/html/mrtg/router.rrd:in:AVERAGE", "DEF:r_out=/var/www/html/mrtg/router.rrd:out:AVERAGE", "LINE1:r_in#0000FF:Packets In\r", "LINE2:r_out#00FF00:Packets Out\r")

while True:
    a5()
    time.sleep(10)
