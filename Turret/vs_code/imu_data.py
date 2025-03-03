import serial
import time


def log_data_to_file(timestamp, yaw, pitch):
    """
    Logs timestamp, yaw, and pitch data into a file.
    """
    with open("yaw_pitch_log.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}, Yaw: {yaw}, Pitch: {pitch}\n")
        print(f"Logged data: Timestamp={timestamp}, Yaw={yaw}, Pitch={pitch}")


# Initialize serial communication
ser = serial.Serial(port='COM8', baudrate=9600, timeout=1)

while True:
    try:
        # Receive IMU message from Pico
        msg_from_pico = ser.readline().decode('utf-8').strip()

        if msg_from_pico:
            print(f"Received: {msg_from_pico}")
            data_parts = msg_from_pico.split(',')

            if len(data_parts) == 3:
                timestamp, yaw, pitch = data_parts
                log_data_to_file(timestamp, yaw, pitch)
            else:
                print("Invalid data format received.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        break
