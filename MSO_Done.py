import pyvisa as visa # https://pyvisa.readthedocs.io/en/latest/
import numpy as np # https://numpy.org/
import time
import matplotlib.pyplot as plt
visaResourceAddr = 'USB0::0x0699::0x052C::SGVJ0002364::INSTR'

rm = visa.ResourceManager()
scope = rm.open_resource(visaResourceAddr)

scope.write("HEADER 0")
scope.write("DATA:SOUR CH1")

scope.write('HORIZONTAL:SCALE 100E-03')
scope.write('CH1:SCALE 100E-03')
#scope.write('VERTICAL:SCALE 1E-02')


scope.write('data:start 1') # first sample
recordLength = int(scope.query('horizontal:recordlength?'))
scope.write('data:stop {}'.format(recordLength)) # last sample
scope.write('wfmoutpre:byt_n 1') # 1 byte per sample
r = scope.write('*opc') # sync

scope.write('acquire:state 0') # stop
scope.write('acquire:stopafter SEQUENCE') # single
scope.write('acquire:state 1') # run
time.sleep(11)
r = scope.query('*opc?') # sync

# Fetch horizontal scaling factors
xinc = float(scope.query("WFMO:XINCR?"))
xzero = float(scope.query("WFMO:XZERO?"))
pt_off = int(scope.query("WFMO:PT_OFF?"))

# Fetch vertical scaling factors
ymult = float(scope.query("WFMO:YMULT?"))
yzero = float(scope.query("WFMO:YZERO?"))
yoff = float(scope.query("WFMO:YOFF?"))

# Fetch waveform data
scope.write("curve?")

# Data is sent back with ieee defined header.  ie. #41000<binary data bytes>\n
# PyVISA read_binary_values() method will automatically read and parse the ieee block header so you don't have to.
rawData = scope.read_binary_values(datatype='b', is_big_endian=False, container=np.ndarray, header_fmt='ieee', expect_termination=True)
dataLen = len(rawData)

# Create numpy arrays of floating point values for the X and Y axis
t0 = (-pt_off * xinc) + xzero
xvalues = np.ndarray(dataLen, np.single)
yvalues = np.ndarray(dataLen, np.single)
for i in range(0,dataLen):
    xvalues[i] = t0 + xinc * i # Create timestamp for the data point
    yvalues[i] = float(rawData[i] - yoff) * ymult + yzero # Convert raw ADC value into a floating point value
    

time.sleep(1)

print("Inrush value from the waveform is : ",float(yvalues.max())/2,"A")
startTime=0
peakTime=0

for i in range(0,dataLen):
    if yvalues[i] == yvalues.max():
        peakTime=xvalues[i]
        for j in range(1,10):
            #print(yvalues[i-j])
            if yvalues[i-j] < 0.1*yvalues.max():
                startTime=xvalues[i-j]
                break

            
if (peakTime-startTime) < 0.001:
    print("Rise time is less than : ",(peakTime-startTime)*2*1000,"ms")
else:
    print("Error in test, do again")

bin_wave = scope.query_binary_values('curve?', datatype='b', container=np.array)
record = int(scope.query('horizontal:recordlength?'))
tscale = float(scope.query('wfmoutpre:xincr?'))
tstart = float(scope.query('wfmoutpre:xzero?'))
vscale = float(scope.query('wfmoutpre:ymult?')) # volts / level
voff = float(scope.query('wfmoutpre:yzero?')) # reference voltage
vpos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)
total_time = tscale * record
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)
unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
scaled_wave = (unscaled_wave - vpos) * vscale + voff



scope.close()
rm.close()

plt.plot(scaled_time, scaled_wave)
plt.title('channel 1') # plot label
plt.xlabel('time (seconds)') # x label
plt.ylabel('voltage (volts)') # y label
print("look for plot window...")
plt.show()
print("\nend of demonstration")
