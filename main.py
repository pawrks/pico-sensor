import network
import socket
import json
import time
import machine
import picozero
from dht import DHT22


# Assign these variables with wi-fi credentials
SSID = ''
PASSWORD = ''

# Define water sensor & DHT22 GPIO pins
# These are the pins that have the data wire of each sensor attached
WATER_SENSOR_PIN = 1
DHT22_PIN = 2

# Zabbix server details
ZABBIX_SERVER_IP = "192.168.1.118"
ZABBIX_SERVER_PORT = 10051
HOST = "pico-sensor"
WATER_KEY = "water_key"
TEMPERATURE_KEY = "f_temp"
HUMIDITY_KEY = "humidity"


def connect_to_wlan():
    # Instantiate WLAN object, STA_IF sets as client to upstream wifi
    wlan = network.WLAN(network.STA_IF)
    
    # Set network interface to up
    wlan.active(True)
    
    # Connect to wifi with creds
    wlan.connect(SSID, PASSWORD)
    
    # Retry connection until connected, flashes on-board LED
    while wlan.isconnected() == False:
        picozero.pico_led.toggle()
        print('Attempting WLAN login... LED will stop flashing when complete.')
        time.sleep(.5)
    
    # Grab ip address from WLAN object and return ip
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def check_wlan_and_reconnect(wlan):
    # Retry connection to wifi if disconnected
    while wlan.isconnected() == False:
        print("Lost connection. Reconnecting...")
        connect_to_wlan()

def send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, key, value):
    # Create a socket object
    # AF_INET sets to IPv4 and SOCK_STREAM sets to TCP
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

# Read water sensor pin and returns 0 for no water and 1 for yes water
def water_sensor():
    water_data = machine.Pin(WATER_SENSOR_PIN, machine.Pin.IN)
    is_water = water_data.value()
    return is_water

# Read DHT22 sensor pin and returns an object with two useful methods
# One method reads temperature and the other humidity
def measure_dht():
    dht22 = DHT22(machine.Pin(DHT22_PIN, machine.Pin.IN))
    dht22.measure()
    return dht22
    

def main():
    # Connect to wifi, return ip to check if still connected in while loop
    ip = connect_to_wlan()
    
    while True:
        try:
            # Check for wifi connection, retries if not successful
            check_wlan_and_reconnect(ip)
            
            # Read water sensor
            is_water = water_sensor()
            
            # Read DHT22 temperature and humidity
            dht22 = measure_dht()
            c_temp = dht22.temperature()
            humidity = dht22.humidity()
            
            # Convert celsius to farenheit
            f_temp = (c_temp * 1.8) + 32
            
            # Send water sensor value to  Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, WATER_KEY, is_water)
            print(f"Water sensor value: {is_water}")
            print("Result:", result)
            
            # Send temperature value to  Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, TEMPERATURE_KEY, f_temp)
            print(f"Temperature: {f_temp} °F")
            print("Result:", result)
            
            # Send humidity value to Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, HUMIDITY_KEY, humidity)
            print(f"Humidity: {humidity} %")
            print("Result:", result)
            
            time.sleep(5)
            
        except Exception as e:
            print(f"An error has occured: {e}")
            print("retrying... ")
            

if __name__ == '__main__':
    main()