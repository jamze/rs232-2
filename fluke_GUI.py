import time
import serial
from datetime import datetime
import tkinter as tk

def time():

    dateTimeObj = datetime.now()
    print(dateTimeObj)
    i = 0
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

def show_values():

    device = device_check.get()
    portCOM = variable_drop.get()
    baudrate = baud_check.get()

    print("Device: ", device, "\nbaudrate: ", baudrate, "\nCOM ", portCOM)

    return device, portCOM, baudrate

def window():

    ### GUI ###

    window = tk.Tk()

    window.title("Data acquisition")

    ### DEVICE ###

    tk.Label(window, text="Choose your device").grid(row=0)
    device_check = tk.IntVar()
    tk.Radiobutton(window, text="Fluke", variable=device_check, value=1).grid(row=1, column=0)
    tk.Radiobutton(window, text="Agilent", variable=device_check, value=2).grid(row=1, column=1)


    ## Fluke = 1
    ## Agilent = 2

    ### COM ###

    tk.Label(window, text="Enter your COM port").grid(row=2)
    variable_drop = tk.IntVar()
    Com_port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    #variable_drop.set(Com_port_list[0])
    port_choose = tk.OptionMenu(window, variable_drop, *Com_port_list).grid(row=2, column=1)


    ### BAUDRATE ###

    tk.Label(tk.Label(window, text="Choose baudrate").grid(row=3))
    baud_check = tk.IntVar()
    tk.Radiobutton(window, text="defult", variable=baud_check, value=115200).grid(row=4, column=0)
    tk.Radiobutton(window, text="115200", variable=baud_check, value=115200).grid(row=4, column=1)
    tk.Radiobutton(window, text="9600", variable=baud_check, value=9600).grid(row=4, column=3)


    ### BUTTONS ###

    tk.Button(window, text="QUIT", command=window.quit).grid(row=7, column=0)
    tk.Button(window, text="test").grid(row=7, column=1)
    tk.Button(window, text="Show", command=show_values).grid(row=7, column=1)

    window.mainloop()
# print("Input COM port number (only number)")
# port_nr=input()
# portCOM=("COM"+port_nr)
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

def configure ():
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=portCOM,
        baudrate=baudrate,
        timeout=0.1,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    #ser.open()
    ser.isOpen()

    print (ser.isOpen())  # check comm

def save_to_file():
    f = open("result.csv", "a")
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

                    f = open("result.csv", "a")
                    print(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                    f.write(str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                    f.close()

                time.sleep(interval)

def start_test():
    show_values()
    configure()
    save_to_file()


### main
window()
start_test()
