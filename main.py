import network
import socket
import machine
import dht
from time import sleep
from picozero import pico_temp_sensor, pico_led


SSID = ''
PASSWORD = ''
SENSOR = dht.DHT22(machine.Pin(2))

def connect_to_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print('Attempting connection to WLAN...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def start_web_server(connection):
    state = 'OFF'
    pico_led.off()
    cpu_temp = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        cpu_temp = pico_temp_sensor.temp
        html = webpage(cpu_temp, state)
        client.send(html)
        print(request)
        print(f'CPU temp: {cpu_temp} degrees celsius')
        client.close()
    
try:
    ip = connect_to_wlan()
    connection = open_socket(ip)
    start_web_server(connection)
except KeyboardInterrupt:
    machine.reset()