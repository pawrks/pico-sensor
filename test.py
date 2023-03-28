import socket
import json
import time
import machine
from dht import DHT22

# Define water sensor ADC pin & DHT22 GPIO pin
WATER_SENSOR_PIN = 26
DHT22_PIN = 15

# Initialize water sensor pin as an ADC input & convert to number between 0-65535
adc = machine.ADC(machine.Pin(WATER_SENSOR_PIN))
water_data = adc.read_u16()

# Initialize the DHT22 sensor
dht22 = DHT22(machine.Pin(DHT22_PIN))

def send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, key, value):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the Zabbix server
    s.connect((zabbix_server_ip, zabbix_server_port))

    # Prepare the data in Zabbix sender protocol format
    data = {
        "request": "sender data",
        "data": [
            {
                "host": host,
                "key": key,
                "value": value
            }
        ]
    }

    # Serialize the data as JSON
    data_json = json.dumps(data)

    # Prepare the data to be sent as a binary packet
    data_to_send = f"{len(data_json):08x}{data_json}".encode()

    # Send the data to the Zabbix server
    s.send(data_to_send)

    # Receive the response from the Zabbix server
    response = s.recv(1024) 

    # Close the socket
    s.close()

    # Parse the response and return the result
    response_json = json.loads(response[13:])
    return response_json["info"]

# Zabbix server details
zabbix_server_ip = ""
zabbix_server_port = 10051
host = ""
water_key = ""
temperature_key = ""
humidity_key = ""

while True:
    # Normalize water data value to a range of 0 to 100
    normalized_value = (water_data * 100) // 65535

    # Measure and read the DHT22 sensor values & set temp to Farenheit
    data = dht22.measure()
    temp = data.temperature()
    f_temp = (temp * 9 / 5) + 32
    humidity = data.humidity()

    # Send water sensor value to  Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, water_key, normalized_value)
    print(f"Water sensor value: {normalized_value}")
    print("Result:", result)

    # Send temperature value to  Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, temperature_key, f_temp)
    print(f"Temperature: {f_temp} °F")
    print("Result:", result)

    # Send humidity value to Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, humidity_key, humidity)
    print(f"Humidity: {humidity} %")
    print("Result:", result)

    # Wait for some time before reading the sensors again
    time.sleep(15)
