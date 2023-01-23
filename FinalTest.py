import pyvisa
import RPi.GPIO as GPIO
import time

rm = pyvisa.ResourceManager()
dmm = rm.open_resource('TCPIP0::10.207.4.80::inst0::INSTR')
in1 = 22 #Power Relay to STK
in2 = 15 #Relay 1
in3 = 16 #Relay 2
in4 = 18 #Relay 3
def quitFast():
	GPIO.cleanup()
	rm.close()
	quit()
def shortCheck(value, TP):
	if value < 1000:
		print("Short found at",TP,".... Terminating program")
		quitFast()
def voltFail(value, lim, TP):
	if value < lim:
		print("Voltage test failed at",TP)


def impCheck(inCh,TP):
	time.sleep(1)
	GPIO.setup(inCh, GPIO.OUT) #GPIO initialise as output
	GPIO.output(inCh, False) #Connect TP to DMM
	for i in range(10):
		val = float(dmm.query(':READ?'))-22600
		time.sleep(0.5)
	shortCheck(val, TP)
	print("Resistance at",TP,"is :"+ str(float("{:.2f}".format(val))) + " ohms")
	time.sleep(1)
	GPIO.output(inCh, True) #Disconnect TP from DMM
		
GPIO.setmode(GPIO.BOARD) #Setting mode of GPIO
dmm.write(':SENS:FUNC "RES"') #Set DMM to measure resistance
GPIO.setup(in1, GPIO.OUT) #GPIO for STK power relay initialise as output

impCheck(in2,"TP1")
impCheck(in3,"TP2")
impCheck(in4,"TP3")

dmm.write(':SENS:FUNC "VOLT"')
time.sleep(0.5)
GPIO.output(in1, False) #Turn on STK

def voltCheck(inCh, TP, lim):
	time.sleep(0.5)
	GPIO.output(inCh, False) #Connect TP to DMM
	for i in range(10):
		val = float(dmm.query(':READ?'))
		time.sleep(0.5)
	print("Voltage at",TP,"is :"+ str(float("{:.3f}".format(val))) + " volts")
	voltFail(val, lim, TP)
	GPIO.output(inCh, True) #Disconnect TP from DMM
	time.sleep(0.5)
	
voltCheck(in2, "TP1", 4.9)
voltCheck(in3, "TP2", 3.2)
voltCheck(in4, "TP3", 3.2)

time.sleep(0.5)
GPIO.output(in1, True) #Turn off STK

GPIO.cleanup()
rm.close()
