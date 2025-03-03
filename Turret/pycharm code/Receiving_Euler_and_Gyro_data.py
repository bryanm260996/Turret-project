import serial
import time

def log_gyro_data(timestamp, gyro_x, gyro_y, gyro_z):
    """
    Logs gyroscope data into a file.
    """
    with open("gyro_log_TEST.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}, Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}\n")
        print(f"Logged Gyro Data: Timestamp={timestamp}, X={gyro_x}, Y={gyro_y}, Z={gyro_z}")

def log_euler_data(timestamp, yaw, pitch, roll):
    """
    Logs Euler angles into a file.
    """
    with open("euler_log_TEST.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}\n")
        print(f"Logged Euler Data: Timestamp={timestamp}, Yaw={yaw}, Pitch={pitch}, Roll={roll}")

# Initialize serial communication
ser = serial.Serial(port='COM8', baudrate=9600, timeout=1)

while True:
    try:
        # Receive IMU message from Pico
        msg_from_pico = ser.readline().decode('utf-8').strip()

        if msg_from_pico:
            print(f"Received: {msg_from_pico}")
            data_parts = msg_from_pico.split(',')

            if data_parts[0] == 'GYRO' and len(data_parts) == 5:
                _, timestamp, gyro_x, gyro_y, gyro_z = data_parts
                log_gyro_data(timestamp, gyro_x, gyro_y, gyro_z)

            elif data_parts[0] == 'EULER' and len(data_parts) == 5:
                _, timestamp, yaw, pitch, roll = data_parts
                log_euler_data(timestamp, yaw, pitch, roll)


    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        break
