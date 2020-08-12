import time
import serial
from datetime import datetime
import tkinter as tk
from threading import Thread

dateTimeObj = datetime.now()
print(dateTimeObj)
timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
time_interval = 1

# def start_measure():
#     global running
#     running = True

def show_values():
    global portCOM
    global device
    global baudrate
    global time_interval
    global stop

    stop = 0

    t = Thread(target=measure)
    t.start()

    device = device_check.get()
    portCOM = str("COM%d" %(variable_drop_COM.get()))
    baudrate = int(variable_drop_baud.get())
    time_interval = int(variable_drop_time.get())

    print("Device: ", device,
          "\nbaudrate: ", baudrate,
          "\nCOM", portCOM,
          "\ntime ", time_interval)

    return device, portCOM, baudrate

def stop_measure():
    global stop
    running = 1

def measure():
    while True:
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port=str(portCOM),
            baudrate=baudrate,
            timeout=0.1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        i = 0
        ser.isOpen()
        input1 = "qm"
        if input1 == 'exit':
            ser.close()
            exit()
        else:
            while 1:
                # send the character to the device
                ser.write((input1 + '\r\n').encode())   ## send command to device
                out = ''
                # let's wait before reading output (let's give device time to answer)
                time.sleep(0.1)
                while ser.inWaiting() > 0:             # waiting for response
                    out = ser.read(99)

                if out != '':
                    string=out.decode()
                    value=string.replace('0\r', ' ')  # stop making 0 after each line

                    valuef=value.split(',')[0]      #delete end of the message (only measurement)
                    valuew=value.split(',')[1]      #what we are measure(ohm/VAC/VDC)

                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
                    i=i+1                           #step

                    f = open("result.csv", "a")
                    print(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                    f.write(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                    f.close()

                #time.sleep(time_interval)               ## This works well
                window.after(1000, measure())

        if stop == 1:
            break



### GUI ###

window = tk.Tk()

window.title("Data acquisition")

### DEVICE ###

tk.Label(window, text="Choose your device").grid(row=0, column=0, pady=20)
device_check = tk.IntVar()
tk.Radiobutton(window, text="Fluke", variable=device_check, value=1).grid(row=0, column=1)
tk.Radiobutton(window, text="Agilent", variable=device_check, value=2).grid(row=0, column=2)

            ## Fluke = 1                ## Agilent = 2


### COM ###

tk.Label(window, text="Enter your COM port").grid(row=2, pady=20)
variable_drop_COM = tk.IntVar()
Com_port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
variable_drop_COM.set(Com_port_list[2])
port_choose = tk.OptionMenu(window, variable_drop_COM, *Com_port_list).grid(row=2, column=1)

### TIME INTERVAL ###

tk.Label(window, text="Choose time interval [s]").grid(row=3, pady=20)
variable_drop_time = tk.IntVar()
time_port_list = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 5, 10]
variable_drop_time.set(time_port_list[5])
time_choose = tk.OptionMenu(window, variable_drop_time, *time_port_list).grid(row=3, column=1)

### BAUDRATE ###


        ## RADIOBUTTON
        #tk.Label(tk.Label(window, text="Choose baudrate").grid(row=4))
        #baud_check = tk.IntVar()
        #tk.Radiobutton(window, text="defult", variable=baud_check, value=115200).grid(row=5, column=0)
        #tk.Radiobutton(window, text="115200", variable=baud_check, value=115200).grid(row=5, column=1)
        #tk.Radiobutton(window, text="9600", variable=baud_check, value=9600).grid(row=5, column=3)

tk.Label(window, text="Choose baudrate").grid(row=4, pady=20)
variable_drop_baud = tk.IntVar()
baud_port_list = [115200, 9600]
variable_drop_baud.set(baud_port_list[0])
baud_choose = tk.OptionMenu(window, variable_drop_baud, *baud_port_list).grid(row=4, column=1)

### COMMAND TO OTHER DEVICES ###

tk.Label(window, text="ADVANCED").grid(row=5, pady=20, columnspan=4)
entry_text = tk.StringVar()

tk.Entry(window, text="lol", textvariable=entry_text).grid(row=6)




### BUTTONS ###

tk.Button(window, text="START TEST", command=measure).grid(row=8, column=0)
tk.Button(window, text="STOP TEST", command=stop_measure).grid(row=8, column=1)
tk.Button(window, text="CONFIRM", command=show_values).grid(row=8, column=2)

window.after(1000, measure)
window.mainloop()

# print("Input COM port number (only number)")
# port_nr=3
# portCOM=("COM3")
# print(portCOM)
#
# print("Input baudrate (defualt for fluke is 115200")
# baud_nr=input()
# print(baud_nr)

# print("Input time interval (min.0.3 sec)")
# time_nr=input()
# delay=0.2
# interval=float(time_nr)-float(delay)

#print(interval)





# print (ser.isOpen())  # check comm
#
# f = open("result.csv", "a")
# # print(timestampStr + "," + valuef + '\r')
# f.write("\r"+"TEST START: "+timestampStr+"\n\rtime,value\r")
# f.close()





# while True:
#  #print ("podaj qm by odczytac wartosci / id by sprawdzic id fluke" / exit by wyjsc)
#     input1 = "qm"
#     if input1 == 'exit':
#         ser.close()
#         exit()
#     else:
#         while 1:
#             # send the character to the device
#             ser.write((input1 + '\r\n').encode())
#             out = ''
#             # let's wait before reading output (let's give device time to answer)
#             time.sleep(0.1)
#             while ser.inWaiting() > 0:             #???
#                 out = ser.read(99)
#
#             if out != '':
#
#                 #print (out)
#                 string=out.decode()
#                 value=string.replace('0\r', ' ')  # stop making 0 after each line
#                 #value = value0r.split("\r")[1]
#                 #print(value)
#
#                 valuef=value.split(',')[0]      #delete end of the message (only measurement)
#                 valuew=value.split(',')[1]      #what we are measure(ohm/VAC/VDC)
#                 #print(valuef)
#
#                 dateTimeObj = datetime.now()
#                 timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
#                 i=i+1                           #step
#
#                 f = open("result.csv", "a")
#                 print(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
#                 f.write(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
#                 f.close()
#
#             time.sleep(time_interval)



