# Pi Pico W Environmentals Sensor

This project is built using MicroPython and the Raspberry Pi Pico W microcontroller along with a variety of sensors. It's purpose is to monitor environmental conditions and send sensor data to a central monitoring solution while remaining reliable and cost-effective.

### Current Features

---

-   Connects Pico W to wi-fi
-   Gathers temperature, and humidity data
-   Creates web socket over HTTP
-   Creates web server and displays sensor data via web browser
-   Turn on-board LED off/on via browser

### Future Plans

---

-   Flash on-board LED while attempting wi-fi connection
-   Keep LED solid color after connection complete
-   Gather water/moisture data, convert ADC output to readable format
-   Connect and send data to Zabbix over SNMP or HTTP

## Requirements

### Hardware

-   [Raspberry Pi Pico WH (includes wireless and headers)](https://www.amazon.com/Pico-Raspberry-Pre-Soldered-Dual-core-Processor/dp/B0BK9W4H2Q/ref=sr_1_3?crid=2B1GNFR12MH6E&keywords=pi+pico+wh&qid=1679514376&s=electronics&sprefix=pi+pico+wh%2Celectronics%2C87&sr=1-3)
-   [DHT22 temperature and humidity sensor](https://www.amazon.com/Gowoops-Temperature-Humidity-Measurement-Raspberry/dp/B073F472JL/ref=sr_1_1?crid=3R6ZHTR2TL1CL&keywords=dht22+sensor+gowoops&qid=1679514476&s=electronics&sprefix=dht22+sensor+gowoops%2Celectronics%2C79&sr=1-1)
-   [Generic water/moisture sensor](https://www.amazon.com/Sensor-Module-Detection-Surface-Arduino/dp/B01N058HS6/ref=asc_df_B01N058HS6/?tag=hyprod-20&linkCode=df0&hvadid=198091640568&hvpos=&hvnetw=g&hvrand=17694561205732239405&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9026834&hvtargid=pla-350450658191&psc=1)
-   [Electrical jumper wires](https://www.amazon.com/EDGELEC-Breadboard-1pin-1pin-Connector-Multicolored/dp/B07GD312VG/ref=sr_1_1_sspa?crid=SUAL3H21O6RR&keywords=female+to+female+jumper+wires&qid=1679514564&s=electronics&sprefix=female+to+female+jumper+wires%2Celectronics%2C88&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyU1czRTBFMDRGQkNTJmVuY3J5cHRlZElkPUEwMDUwNjMxVE5MOVYyUzRZNUhMJmVuY3J5cHRlZEFkSWQ9QTAyMTc1NDZRQVJERDNEQzgxM1Mmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl)
-   [Protective case for Pico](https://www.amazon.com/C4Labs-Zebra-Pico-Case-Raspberry/dp/B08X24QJZC/ref=sr_1_3?crid=3L7RQXKD6KT72&keywords=pi+pico+case&qid=1679515852&s=electronics&sprefix=pi+pico+case%2Celectronics%2C108&sr=1-3)
-   Wi-fi network with login credentials
-   PC to connect to Pi Pico
-   USB A/C to Micro-B cable (included with Pico link above)

### Software

-   Text editor such as [Thonny](https://thonny.org/) or [VS Code](https://code.visualstudio.com/download)
-   Latest [UF2 firmware for Pi Pico W](https://rpf.io/pico-w-firmware) (click to download on local machine) you can also install via [MicroPython](https://micropython.org/download/rp2-pico-w/) or [Raspberry Pi](https://www.raspberrypi.org/)
-   Modules from PyPi (will expand on this later)
-   [Zabbix](https://www.zabbix.com/) (current version of pico_sensor not supported)

Note: Thonny text editor is beginner friendly while VS Code is a more advanced option.

**This project is a work in progress and will continue to be updated.**
