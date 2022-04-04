
import time
import random
import requests as re
from datetime import datetime
import json
import board
import adafruit_dht

def start_recording():
    wait_int = 2
    itter_time = 5 * wait_int
    init = True
    tot_time = 0

    while True:
        
        if init == False:
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
            tot_time += time_sum
            
            # reset if time is greater than 1 day
            if tot_time > 86400:
                tot_time = 0
            
            
            try: 
                # send API request
                avg_temp = sum(temps) / len(temps)
                avg_humid  = sum(humids) / len(humids)
                
                print("avg_temp ", avg_temp)
                print("avg_humid ", avg_humid)
                print("total time seconds ", tot_time)
                
                
                payload = {   "sensor_timestamp": str(timestamp),
                            "temperature": avg_temp,
                            "humidity": avg_humid,
                            "time": tot_time}
                url = "https://lt65wmhz4i.execute-api.us-east-2.amazonaws.com/Prod/sensor/dht"
                
                r = re.post(url, json=payload)
                
                print(r)
            except:
                print("error sending API request")
            
            # reset itteration
            time_sum = 0
            temps = []
            humids = []
            
            
        if init == True:
            time_sum = 0
            temps = []
            humids = []

            
        init = False

        while time_sum < itter_time:

            try:
                # Print the values to the serial port
                #temperature_c = random.choice([25, 27, 30])
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                #humidity = random.choice([25, 27, 30])
                humidity = dhtDevice.humidity
                print(
                    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                        temperature_f, temperature_c, humidity
                    )
                )

                print(temperature_f)
                temps.append(temperature_f)
                print(temps)
                humids.append(humidity)

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(wait_int)
                time_sum += wait_int
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error

            time_sum += wait_int
            time.sleep(wait_int)
        
if __name__ == "__main__":
    
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    start_recording()