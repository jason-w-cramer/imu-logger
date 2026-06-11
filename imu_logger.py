import serial
import csv
from datetime import datetime

PORT = 'COM10'        # change to your port, on Linux it's something like '/dev/ttyACM0'
BAUD = 115200
OUTPUT_FILE = 'imu_log.csv'

with serial.Serial(PORT, BAUD, timeout=1) as ser:
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'])
        
        print(f"Logging to {OUTPUT_FILE}. Press Ctrl+C to stop.")
        
        while True:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            
            try:
                # parse "Ax:0.01 Ay:0.00 Az:1.00 Gx:0.12 Gy:-0.03 Gz:0.01"
                values = {}
                for part in line.split():
                    key, val = part.split(':')
                    values[key] = float(val)
                
                row = [
                    datetime.now().isoformat(),
                    values['Ax'], values['Ay'], values['Az'],
                    values['Gx'], values['Gy'], values['Gz']
                ]
                writer.writerow(row)
                csvfile.flush()
                print(row)
                
            except (ValueError, KeyError):
                continue  # skip malformed lines