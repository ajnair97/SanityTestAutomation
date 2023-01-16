import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
print("Starting Program 1: Impedance check")
i2c = busio.I2C(board.SCL, board.SDA)
ads=ADS.ADS1115(i2c)
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
chan3 = AnalogIn(ads, ADS.P2)
chan4 = AnalogIn(ads, ADS.P3)
#while True:
 #   print("CHAN 1: "+"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
  #  print("CHAN 2: "+"{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
   # print("CHAN 3: "+"{:>5}\t{:>5.3f}".format(chan3.value, chan3.voltage))
    #print("CHAN 4: "+"{:>5}\t{:>5.3f}".format(chan4.value, chan4.voltage))
    #time.sleep(1)
i=0
#while i<20:
#    time.sleep(1)
#    if chan1.voltage < 0.100 :
#        print("Channel 1 short found")
#    else :
#        print("Channel 1 is OK")
#        print("CHAN 1: "+"{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
#    i=i+1
ch1 = ch2 = ch3 = ch4 = 'T'
while i<10:
    if chan1.voltage < 0.100 :
        ch1='F'
        print("Channel 1 failed")
        #break
    if chan2.voltage < 0.100 :
        ch2='F'
        print("Channel 2 failed")
        #break
    if chan3.voltage < 0.100 :
        ch3='F'
        print("Channel 3 failed")
        #break
    if chan4.voltage < 0.100 :
        ch4='F'
        print("Channel 4 failed")
        #break
    i=i+1
    time.sleep(0.5)
print("Program 1 ended")
if (ch1 =='F' or ch2=='F' or ch3=='F' or ch4=='F'):
    print("Impedance check failed")
    quit()
elif (ch1 =='T' or ch2=='T' or ch3=='T' or ch4=='T'):
    print("Impedance check passed")
else:
    print("Program failed")
time.sleep(3)
print("Starting Program 2: Voltage check")
time.sleep(2)
in1 = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.output(in1,False) #relay ON
print("Board turned ON")
time.sleep(5)
GPIO.output(in1, True)#relay OFF
print("Board turned OFF")

    
