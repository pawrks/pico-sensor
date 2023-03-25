import socket
import json
import time
import machine
from dht import DHT22

# Define the water sensor ADC pin number
WATER_SENSOR_PIN = 26  # Replace with the ADC pin number you connected the water sensor to

# Initialize the water sensor pin as an ADC input
adc = machine.ADC(machine.Pin(WATER_SENSOR_PIN))
water_sensor = adc.read_u16()

# Define the DHT22 sensor GPIO pin number
DHT22_PIN = 15  # Replace with the GPIO pin number you connected the DHT22 sensor to

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

# Replace these variables with your Zabbix server details
zabbix_server_ip = "YOUR_ZABBIX_SERVER_IP"
zabbix_server_port = 10051
host = "YOUR_HOST_NAME"
water_key = "YOUR_WATER_ITEM_KEY"
temperature_key = "YOUR_TEMPERATURE_ITEM_KEY"
humidity_key = "YOUR_HUMIDITY_ITEM_KEY"

while True:

    # Normalize the value to a range of 0 to 100
    normalized_value = (water_sensor * 100) // 65535

    # Read the DHT22 sensor values
    temperature, humidity = dht22.measure()

    # Send the water sensor value to the Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, water_key, normalized_value)
    print(f"Water sensor value: {normalized_value}")
    print("Result:", result)

    # Send the temperature value to the Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, temperature_key, temperature)
    print(f"Temperature: {temperature} °C")
    print("Result:", result)

    # Send the humidity value to the Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, humidity_key, humidity)
    print(f"Humidity: {humidity} %")
    print("Result:", result)

    # Wait for some time before reading the sensors again
    time.sleep(15)  # Adjust the delay as needed
