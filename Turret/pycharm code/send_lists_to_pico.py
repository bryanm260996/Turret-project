import serial

ser=serial.Serial()
ser.baudrate=9600
ser.port = 'COM4'
ser.open()

numbers= b"1,3,4,5,3,2\n"

#PACKAGE MESSAGE
#separator is: ,
tx_msg = numbers
ser.write(tx_msg)

