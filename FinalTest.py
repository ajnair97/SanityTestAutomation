import pyvisa
import RPi.GPIO as GPIO
import time
rm = pyvisa.ResourceManager()
dmm = rm.open_resource('TCPIP0::10.207.4.80::inst0::INSTR')
in1 = 22 #Power Relay to STK
in2 = 15 #Relay 1
in3 = 16 #Relay 2
in4 = 18 #Relay 3


GPIO.setmode(GPIO.BOARD) #Setting mode of GPIO
GPIO.setup(in1, GPIO.OUT) #GPIO initialise as output


#
#time.sleep(1)
#GPIO.output(in1, True)
#dmm.write('*RST')
dmm.write(':SENS:FUNC "RES"')

time.sleep(1)
GPIO.setup(in2, GPIO.OUT) #GPIO initialise as output
GPIO.output(in2, False) #Connect first TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))-22600
	time.sleep(0.5)
print("Resistance at first TP: " + str(float("{:.2f}".format(val))) + " ohms")
time.sleep(1)
GPIO.output(in2, True) #Disconnect TP1 from DMM

time.sleep(0.5)
GPIO.setup(in3, GPIO.OUT) #GPIO initialise as output
GPIO.output(in3, False) #Connect second TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))-22600
	time.sleep(0.5)
print("Resistance at second TP: " + str(float("{:.2f}".format(val))) + " ohms")
time.sleep(1)
GPIO.output(in3, True) #Disconnect TP2 from DMM

time.sleep(0.5)
GPIO.setup(in4, GPIO.OUT) #GPIO initialise as output
GPIO.output(in4, False) #Connect third TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))-22600
	time.sleep(0.5)
print("Resistance at third TP: " + str(float("{:.2f}".format(val))) + " ohms")
time.sleep(1)
GPIO.output(in4, True) #Disconnect TP3 from DMM

#dmm.write('*RST')
dmm.write(':SENS:FUNC "VOLT"')
time.sleep(0.5)
GPIO.output(in1, False) #Turn on STK

time.sleep(1)
GPIO.output(in2, False) #Connect first TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))
	time.sleep(0.5)
print("Voltage at first TP: " + str(float("{:.2f}".format(val))) + " volts")
time.sleep(1)
GPIO.output(in2, True) #Disconnect TP1 from DMM
time.sleep(0.5)

GPIO.output(in3, False) #Connect second TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))
	time.sleep(0.5)
print("Voltage at second TP: " + str(float("{:.2f}".format(val))) + " volts")
time.sleep(1)
GPIO.output(in3, True) #Disconnect TP2 from DMM
time.sleep(0.5)

GPIO.output(in4, False) #Connect third TP to DMM
for i in range(10):
	val = float(dmm.query(':READ?'))
	time.sleep(0.5)
print("Voltage at third TP: " + str(float("{:.2f}".format(val))) + " volts")
time.sleep(1)
GPIO.output(in4, True) #Connect third TP to DMM
time.sleep(0.5)
GPIO.output(in1, True) #Turn off STK














GPIO.cleanup()
rm.close()
