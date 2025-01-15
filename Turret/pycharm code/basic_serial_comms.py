
#THIS CODE IS THE MOST BASIC SERIAL COMMS SETUP

import serial

ser=serial.Serial()
ser.baudrate=9600
ser.port = 'COM4'
ser.open()

#send message to pico
msg_to_pico= b"This is Bryan and Ava\n"
ser.write(msg_to_pico)

#receive message to pico
msg_from_pico= ser.readline()
print(msg_from_pico)
#close the port
ser.close()