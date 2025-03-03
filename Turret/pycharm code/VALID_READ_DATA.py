import serial
import time

def log_data_to_file(timestamp, x, y):
    """
    Logs timestamp, x, and y data into a file.
    """
    try:
        with open("VALID_log_position_YAW.txt", "a") as file:
            file.write(f"Timestamp: {timestamp}, x: {x}, y: {y}\n")
            print(f"Logged data: Timestamp: {timestamp}, x: {x}, y: {y}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Initialize serial communication
ser = serial.Serial(port='COM8', baudrate=9600, timeout=1)

while True:
    try:
        # Receive IMU message from Pico
        msg_from_pico = ser.readline().decode('utf-8').strip()

        if msg_from_pico:
            print(f"Received: {msg_from_pico}")
            data_parts = msg_from_pico.split(',')

            # Check that we have exactly 3 parts (timestamp, x, y)
            if len(data_parts) == 3:
                timestamp, x, y = data_parts
                log_data_to_file(timestamp, x, y)


        time.sleep(0.1)  # Add a small delay to avoid overloading the CPU

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        break
