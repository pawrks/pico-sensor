import network
import socket
import json
import time
import machine
import picozero
from dht import DHT22


SSID = 'customer.gipnetworks.com'
PASSWORD = '2008012345'

def connect_to_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        picozero.pico_led.toggle()
        print('Attempting WLAN login... LED will stop flashing when complete.')
        time.sleep(.5)
        
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Define water sensor ADC pin & DHT22 GPIO pin
WATER_SENSOR_PIN = 1
DHT22_PIN = 2

# Initialize water sensor & DHT22 sensor pins
water_data = machine.Pin(WATER_SENSOR_PIN, machine.Pin.IN)
dht22 = DHT22(machine.Pin(DHT22_PIN, machine.Pin.IN))

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
    print(data_json)

    # Prepare the data to be sent as a binary packet
    zabbix_header = b'ZBXD\x01'
    data_len = len(data_json)
    data_to_send = zabbix_header + data_len.to_bytes(8, 'little') + data_json.encode()

    # Send the data to the Zabbix server
    s.sendall(data_to_send)

    # Receive the response from the Zabbix server
    response = s.recv(1024)
    print(response)

    # Close the socket
    s.close()

    # Parse the response and return the result
    response_json = json.loads(response[13:])
    return response_json["info"]
# 
# Zabbix server details
zabbix_server_ip = "192.168.1.118"
zabbix_server_port = 10051
host = "pico-sensor"
water_key = "water_key"
temperature_key = "f_temp"
humidity_key = "humidity"

connect_to_wlan()

while True:
    # Measure and read water sensor; 0 => False and 1 => True
    is_water = water_data.value()

    # Measure and read the DHT22 sensor values and set temp to Farenheit
    dht22.measure()
    temp = dht22.temperature()
    f_temp = (temp * 9 / 5) + 32
    humidity = dht22.humidity()

    # Send water sensor value to  Zabbix server
    result = send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, water_key, is_water)
    print(f"Water sensor value: {is_water}")
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
    time.sleep(5)
