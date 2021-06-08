import serial
import time
import threading
import serial.tools.list_ports

# List all available COM port
[print(port) for port in serial.tools.list_ports.comports() if port[2] != 'n/a']

print('Choose COM port:')
port_num = input()

ser = serial.Serial()
ser.port = "COM" + port_num

#115200,N,8,1
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check
ser.stopbits = serial.STOPBITS_ONE #number of stop bits

ser.timeout = 0.5          #non-block read 0.5s
ser.writeTimeout = 0.5     #timeout for write 0.5s
ser.xonxoff = False    #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control


try: 
    ser.open()
except Exception as ex:
    print ("open serial port error " + str(ex))
    exit()

def read_serial():
    while 1:
        # Wait until there is data waiting in the serial buffer
        if(ser.in_waiting > 0):
            # serialString = ser.readline()
            serialData = ser.read()

            # Print the contents of the serial data
            try:
                # print(serialString.decode('Ascii'))
                print(serialData)
            except:
                continue

def isEven(num):
    if num%2 == 0:
        return True
    else:
        return False

def write_serial():
    while 1:
        val = input()
        if val == '' or isEven(len(val)) != True:
            continue

        for i in range(0, len(val)-1, 2):
            if int('0x'+val[i:i+2], 16) < 256:
                out = [int(val[i:i+2], 16)]
                print(bytes(out))
                ser.write(bytes(out))
            time.sleep(0.01)

read_thread = threading.Thread(target=read_serial)
write_thread = threading.Thread(target=write_serial)

read_thread.start()
write_thread.start()
