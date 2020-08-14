import time
import serial
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Thread

dateTimeObj = datetime.now()
print(dateTimeObj)
timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

global running
running = 0                          # variable to control measurement loop START 1 / STOP 2
confirmed = 0

def show_values():

    global portCOM
    global device
    global baudrate
    global time_interval
    global running
    global command
    global confirmed

    ### need to assign values after setting to memory ###

    device = device_check.get()
    portCOM = str("COM%d" %(variable_drop_COM.get()))
    baudrate = int(variable_drop_baud.get())
    time_interval = float(variable_drop_time.get())-0.1
    command = str(e1.get())
    confirmed = 1

    print("Device: ", device,
          "\nbaudrate: ", baudrate,
          "\nCOM", portCOM,
          "\ntime interval ", time_interval,
          "\nrunning: ", running,
          "\nentry: ", command)


# def connect():
#     while connect == 1:
#             # configure the serial connections (the parameters differs on the device you are connecting to)
#             ser = serial.Serial(
#                 port=str(portCOM),
#                 baudrate=baudrate,
#                 timeout=0,  # check how low we can get -> 0 works :D
#                 parity=serial.PARITY_NONE,
#                 stopbits=serial.STOPBITS_ONE,
#                 bytesize=serial.EIGHTBITS
#             )
#
#             i = 0
#
#             ser.isOpen()


def measure():
    while running == 1:
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port=str(portCOM),
            baudrate=baudrate,
            timeout=0,                #check how low we can get -> 0 works :D
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        i = 0

        ser.isOpen()
        # print(ser.isOpen())

        result_window.delete(1.0, tk.END)
        input1 = str(command)
        if input1 == "exit":
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
                    string = out.decode()
                    value = string.replace('0\r', ' ')  # stop making 0 after each line

                    valuef = value.split(',')[0]      #delete end of the message (only measurement)
                    valuew = value.split(',')[1]      #what we are measure(ohm/VAC/VDC)

                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
                    i=i+1                           #step

                    f = open("result.csv", "a")
                    print(str(i)+", " +timestampStr+","+valuef +", "+valuew +'\r')
                    f.write(str(i)+", " +timestampStr+","+valuef +", "+valuew +'\r')
                    # results.insert(0, str(i)+"," +timestampStr+","+valuef +","+valuew +'\r')
                    result_window.insert(tk.END, str(i)+", " +timestampStr+","+valuef +", "+valuew +'\n')
                    f.close()

                time.sleep(time_interval)
                if break_loop == 1:
                    break

def stop_measure():
    global running
    global break_loop

    running = 0
    break_loop = 1

    command = "exit"

def start_measure():
    global running
    global break_loop
    global confirmed

    #running = 1
    # break_loop = 0

    if confirmed:
        t = Thread(target=measure)
        t.start()
        running = 1
        break_loop = 0
    else:
        messagebox.showinfo("WARNING", "please CONFIRM first")

### GUI ###

window = tk.Tk()
window.title("Data acquisition")

tk.Label(window,
         text="Program for data acquisition from multimeter to PC in form of csv file").grid(row=0,
                                                                                             columnspan=4)

window.columnconfigure(0, minsize=150)
window.columnconfigure(1, minsize=100)
window.columnconfigure(2, minsize=100)
window.columnconfigure(3, minsize=50)


### DEVICE ###

tk.Label(window, text="Choose your device").grid(row=5, column=0, pady=20, sticky="nswe")
device_check = tk.IntVar()
tk.Radiobutton(window, text="Fluke", variable=device_check, value=1).grid(row=5, column=1)
tk.Radiobutton(window, text="Agilent", variable=device_check, value=2).grid(row=5, column=2)

            ## Fluke = 1    ## Agilent = 2

### COM ###

tk.Label(window, text="Enter your COM port").grid(row=10, pady=20)
variable_drop_COM = tk.IntVar()
Com_port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
variable_drop_COM.set(Com_port_list[2])
port_choose = tk.OptionMenu(window, variable_drop_COM, *Com_port_list).grid(row=10, column=1, sticky="we")

### TIME INTERVAL ###

tk.Label(window, text="Choose time interval [s]").grid(row=20, pady=20, sticky="nswe")
variable_drop_time = tk.DoubleVar()
time_port_list = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 5, 10, 20, 30]
variable_drop_time.set(time_port_list[5])
time_choose = tk.OptionMenu(window, variable_drop_time, *time_port_list).grid(row=20, column=1, sticky="we")

### BAUDRATE ###

tk.Label(window, text="Choose baudrate").grid(row=30, pady=20, sticky="we")
variable_drop_baud = tk.IntVar()
baud_port_list = [115200, 57600, 38400, 19200, 9600]
variable_drop_baud.set(baud_port_list[0])
baud_choose = tk.OptionMenu(window, variable_drop_baud, *baud_port_list).grid(row=30, column=1, sticky="we")

### COMMAND TO OTHER DEVICES ###

tk.Label(window, text="!!! ADVANCED !!!", font='bold').grid(row=40, columnspan=4)
tk.Label(window, text="!!! If you are not sure "
                      "what to send leave this as default !!!").grid(row=41, columnspan=4, pady=(10, 0))
tk.Label(window, text="put here your own command to the device").grid(row=42, columnspan=4, pady=(0, 0))
entry_text = tk.StringVar()

e1 = tk.Entry(window,textvariable=entry_text)
e1.insert(0,"qm")
e1.grid(row=50, columnspan=4, rowspan=4, pady=20, sticky="nswe")

### BUTTONS ###

tk.Button(window, text="1. CONFIRM", command=show_values).grid(row=100, column=0, sticky="nswe")
tk.Button(window, text="2. START TEST", command=start_measure).grid(row=100, column=1, sticky="nswe")
tk.Button(window, text="3. STOP TEST", command=stop_measure).grid(row=100, column=2, sticky="nswe")
tk.Button(window, text="QUIT", command=quit).grid(row=100, column=3, sticky="nswe")

### RESULTS ###

tk.Label(window, text="RESULTS", font="bold").grid(row=125, column=0, pady=10, columnspan=4, sticky="nswe")
#result_window = tk.Text(window, height=10, width=10) WORK
result_window = tk.scrolledtext.ScrolledText(window, height=10, width=10)
result_window.grid(row=126, column=0, columnspan=4, sticky="nswe")
tk.Scrollbar(window)

window.mainloop()
