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
ZABBIX_SERVER_IP = '192.168.1.118'
ZABBIX_SERVER_PORT = 10051
HOST = 'pico-sensor'
WATER_KEY = 'water_key'
TEMPERATURE_KEY = 'f_temp'
HUMIDITY_KEY = 'humidity'


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
    return wlan

def check_wlan_and_reconnect(wlan):
    # Retry connection to wifi if disconnected
    while wlan.isconnected() == False:
        print('Lost connection. Reconnecting...')
        connect_to_wlan()
        
def water_sensor():
    # Read water sensor pin; returns 0 for no water and 1 for yes water
    water_data = machine.Pin(WATER_SENSOR_PIN, machine.Pin.IN)
    is_water = water_data.value()
    return is_water

def measure_dht():
    # Read DHT22 sensor pin and returns an object with two useful methods
    # One method reads temperature and the other humidity
    dht22 = DHT22(machine.Pin(DHT22_PIN, machine.Pin.IN))
    dht22.measure()
    return dht22

def send_data_to_zabbix_server(zabbix_server_ip, zabbix_server_port, host, key, value):
    # Create socket object
    # AF_INET sets to IPv4 and SOCK_STREAM sets to TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to Zabbix server
    s.connect((zabbix_server_ip, zabbix_server_port))

    # Prepare data in Zabbix sender protocol format
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

    # Serialize data as JSON
    data_json = json.dumps(data)
    print(data_json)

    # Prepare data to be sent as a binary packet
    zabbix_header = b'ZBXD\x01'
    data_len = len(data_json)
    data_to_send = zabbix_header + data_len.to_bytes(8, 'little') + data_json.encode()

    # Send data to Zabbix server
    s.sendall(data_to_send)

    # Receive response from Zabbix server
    response = s.recv(1024)
    print(response)

    # Close socket
    s.close()

    # Parse response and return result
    response_json = json.loads(response[13:])
    return response_json['info']
    

def main():
    # Connect to wifi, return wlan object to check if still connected in while loop
    wlan = connect_to_wlan()
    
    while True:
        # Try except block checks for wi-fi and sensor failures
        # No logging saved on pico-sensor, all data stored in memory and sent to Zabbix
        # Zabbix alerts can be modified to activate under certain conditions
        try:
            # Check for and retry wi-fi connection if connection is lost
            check_wlan_and_reconnect(wlan)
            
            # Read water sensor
            is_water = water_sensor()
            
            # Read DHT22 temperature and humidity
            dht22 = measure_dht()
            c_temp = dht22.temperature()
            humidity = dht22.humidity()
            
            # Convert celsius to farenheit
            f_temp = (c_temp * 1.8) + 32
            
            # Added 4 x 1 second timers to not overload Pico
            # These split the sensor logic and each send_data_to_zabbix_server
            time.sleep(1)
            
            # Send water sensor value to  Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, WATER_KEY, is_water)
            print(f'Water sensor value: {is_water}')
            print('Result:', result)
            time.sleep(1)
            
            # Send temperature value to  Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, TEMPERATURE_KEY, f_temp)
            print(f'Temperature: {f_temp} °F')
            print('Result:', result)
            time.sleep(1)
            
            # Send humidity value to Zabbix server
            result = send_data_to_zabbix_server(ZABBIX_SERVER_IP, ZABBIX_SERVER_PORT, HOST, HUMIDITY_KEY, humidity)
            print(f'Humidity: {humidity} %')
            print('Result:', result)
            time.sleep(1)
            
        except Exception as e:
            print(f'An error has occured: {e}')
            print('retrying... ')
            

if __name__ == '__main__':
    main()