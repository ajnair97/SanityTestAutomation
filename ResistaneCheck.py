import pyvisa
import time
rm = pyvisa.ResourceManager()
dmm = rm.open_resource('USB0::0x05E6::0x7510::04570591::INSTR')
dmm.write('*RST')
dmm.write(':SENS:FUNC "RES"')
for i in range(11):
    
    val=float(dmm.query(':READ?'))-22600
    if i>2:
        print(float("{:.2f}".format(val)))
    time.sleep(1)
dmm.write('*RST')
dmm.write(':SENS:FUNC "VOLT"')
for i in range(11):
    
    val=float(dmm.query(':READ?'))
    if i>2:
        print(float("{:.2f}".format(val)))
    time.sleep(1)
    
