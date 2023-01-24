import pyvisa
import RPi.GPIO as GPIO
import time
from csv import writer
rm = pyvisa.ResourceManager()
dmm = rm.open_resource('TCPIP0::10.207.4.80::inst0::INSTR')
in1 = 22 #Power Relay to STK
in2 = 15 #Relay 1
in3 = 16 #Relay 2
in4 = 18 #Relay 3
brdID = input("Enter the Board model [BRDXXXX] : ")
slNo = input("Enter the serial number of the board : ")
imp='Pass'
vol='Pass'
def writeCSV(lis):
	with open('/home/ajnair/Documents/database.csv', 'a') as f_object:
		writer_object = writer(f_object)
		writer_object.writerow(lis)
		f_object.close()		
    
def quitFast():
	GPIO.cleanup()
	rm.close()
	quit()
def shortCheck(value, TP):
	if value < 1000:
		imp='Fail'
		print("Short found at",TP,".... Terminating program")
		data = [brdID, slNo, 'Fail', 'Not checked']
		writeCSV(data)
		quitFast()
		
def voltFail(value, lim, TP):
	if value < lim:
		print("Voltage test failed at",TP)
		global vol
		vol ='Fail'		

def voltFailUp(value, lim, TP):
	if value > lim:
		print("Voltage test failed at",TP)
		global vol
		vol ='Fail'	

def impCheck(inCh,TP):
	time.sleep(1)
	GPIO.setup(inCh, GPIO.OUT) #GPIO initialise as output
	GPIO.output(inCh, False) #Connect TPx to DMM
	for i in range(10):
		val = float(dmm.query(':READ?'))-22600
		time.sleep(0.5)
	shortCheck(val, TP)
	print("Resistance at",TP,"is :"+ str(float("{:.2f}".format(val))) + " ohms")
	time.sleep(1)
	GPIO.output(inCh, True) #Disconnect TPx from DMM
		
GPIO.setmode(GPIO.BOARD) #Setting mode of GPIO
dmm.write(':SENS:FUNC "RES"') #Set DMM to measure resistance
GPIO.setup(in1, GPIO.OUT) #GPIO for STK power relay initialise as output

impCheck(in2,"TP1")
impCheck(in3,"TP2")
impCheck(in4,"TP3")
input("Insert next 3 testpoints and press enter...")
impCheck(in2,"TP4")
impCheck(in3,"TP5")
impCheck(in4,"TP6")
input("Insert next 3 testpoints and press enter...")
impCheck(in2,"TP9")
impCheck(in3,"TP10")
impCheck(in4,"TP11")
#input("Insert next 3 testpoints and press enter...")
#impCheck(in2,"TP10")

dmm.write(':SENS:FUNC "VOLT"')
time.sleep(0.5)
input("Connect TP1, TP2 and TP3 ")
GPIO.output(in1, False) #Turn on STK

def voltCheck(inCh, TP, lim):
	time.sleep(0.5)
	GPIO.output(inCh, False) #Connect TPx to DMM
	for i in range(10):
		val = float(dmm.query(':READ?'))
		time.sleep(0.5)
	print("Voltage at",TP,"is :"+ str(float("{:.3f}".format(val))) + " volts")
	voltFail(val, lim, TP)
	GPIO.output(inCh, True) #Disconnect TPx from DMM
	time.sleep(0.5)
	
def voltCheckUp(inCh, TP, lim):
	time.sleep(0.5)
	GPIO.output(inCh, False) #Connect TPx to DMM
	for i in range(10):
		val = float(dmm.query(':READ?'))
		time.sleep(0.5)
	print("Voltage at",TP,"is :"+ str(float("{:.3f}".format(val))) + " volts")
	voltFailUp(val, lim, TP)
	GPIO.output(inCh, True) #Disconnect TPx from DMM
	time.sleep(0.5)

input("Connect TP1, TP2 and TP3 ")
voltCheck(in2, "TP1", 3.2)
voltCheckUp(in2, "TP1", 3.4)
voltCheck(in3, "TP2", 3.2)
voltCheckUp(in3, "TP2", 3.4)
voltCheck(in4, "TP3", 3.2)
voltCheckUp(in4, "TP3", 3.4)
input("Insert next 3 testpoints and press enter...")
voltCheck(in2, "TP4", 4.9)
voltCheckUp(in2, "TP4", 5.1)
voltCheck(in3, "TP5", 3.2)
voltCheckUp(in3, "TP5", 3.4)
voltCheck(in4, "TP6", 3.5)
voltCheckUp(in4, "TP6", 3.7)
input("Insert next 3 testpoints and press enter...")
voltCheck(in2, "TP9", 2.15)
voltCheckUp(in2, "TP9", 2.35)
voltCheck(in3, "TP10", 1.7)
voltCheckUp(in3, "TP10", 1.9)
voltCheck(in4, "TP11", 3.2)
voltCheckUp(in4, "TP11", 3.4)

if vol=='Fail':
	data = [brdID, slNo, 'Pass', 'Fail']
	writeCSV(data)
	

time.sleep(0.5)
GPIO.output(in1, True) #Turn off STK

GPIO.cleanup()
rm.close()
