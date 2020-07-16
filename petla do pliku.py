import time
import serial
from datetime import datetime
dateTimeObj = datetime.now()
print(dateTimeObj)
i=0

timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    timeout=0.1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#ser.open()
ser.isOpen()

#print (ser.isOpen())  # check comm

f = open("result.txt", "a")
# print(timestampStr + "," + valuef + '\r')
f.write("\r"+"TEST START: "+timestampStr+"\n\rtime,value\r")
f.close()

while 1:
 #print ("podaj qm by odczytac wartosci / id by sprawdzic id fluke" / exit by wyjsc)
    input1 = "qm"
    if input1 == 'exit':
        ser.close()
        exit()
    else:
        while 1:
            # send the character to the device
            ser.write((input1 + '\r\n').encode())
            out = ''
            # let's wait before reading output (let's give device time to answer)
            time.sleep(0.1)
            while ser.inWaiting() > 0:             #???
                out = ser.read(99)

            if out != '':

                #print (out)
                string=out.decode()
                value=string.replace('0\r', ' ')  # stop making 0 after each line
                #value = value0r.split("\r")[1]
                #print(value)

                valuef=value.split(',')[0]      #delete end of the message (only measurement)
                valuew=value.split(',')[1]      #what we are measure(ohm/VAC/VDC)
                #print(valuef)

                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
                i=i+1                           #step

                f = open("result.txt", "a")
                print(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                f.write(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                f.close()

            time.sleep(0.1)
