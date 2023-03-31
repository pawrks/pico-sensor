# Pi Pico W Environmentals Sensor

This project is built using MicroPython and the Raspberry Pi Pico W microcontroller along with a variety of sensors. It's purpose is to monitor environmental conditions and send sensor data to a central monitoring solution (Zabbix) while remaining reliable and cost-effective.

---

### Current Features

-   Ultra low hardware cost - at time of purchase in 2023 it was just under $25 per "Pico sensor" (does not include case or PoE to USB power supply)
-   No traditional operating system, it only runs Python
-   Connects Pico W to wi-fi
-   On-board LED flashes while attempting wi-fi connection
-   Gathers and reads water sensor, humidity, and temperature data
-   Converts all sensor data to binary packet readable by Zabbix
-   Connects to Zabbix via network socket and sends data with Zabbix sender protocol
-   Includes error handling for maximum up-time
-   Enclosure for protecting the Pico

### Future Plans

-   Update documentation with instructions to get fully up and running

---

## Requirements

### Hardware

-   [Raspberry Pi Pico WH (includes wireless and headers)](https://www.amazon.com/Pico-Raspberry-Pre-Soldered-Dual-core-Processor/dp/B0BK9W4H2Q/ref=sr_1_3?crid=2B1GNFR12MH6E&keywords=pi+pico+wh&qid=1679514376&s=electronics&sprefix=pi+pico+wh%2Celectronics%2C87&sr=1-3)
-   [DHT22 humidity and temperature sensor](https://www.amazon.com/Gowoops-Temperature-Humidity-Measurement-Raspberry/dp/B073F472JL/ref=sr_1_1?crid=3R6ZHTR2TL1CL&keywords=dht22+sensor+gowoops&qid=1679514476&s=electronics&sprefix=dht22+sensor+gowoops%2Celectronics%2C79&sr=1-1)
-   [Generic water/moisture sensor](https://www.amazon.com/Sensor-Module-Detection-Surface-Arduino/dp/B01N058HS6/ref=asc_df_B01N058HS6/?tag=hyprod-20&linkCode=df0&hvadid=198091640568&hvpos=&hvnetw=g&hvrand=17694561205732239405&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9026834&hvtargid=pla-350450658191&psc=1)
-   [Electrical jumper wires](https://www.amazon.com/EDGELEC-Breadboard-1pin-1pin-Connector-Multicolored/dp/B07GD312VG/ref=sr_1_1_sspa?crid=SUAL3H21O6RR&keywords=female+to+female+jumper+wires&qid=1679514564&s=electronics&sprefix=female+to+female+jumper+wires%2Celectronics%2C88&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyU1czRTBFMDRGQkNTJmVuY3J5cHRlZElkPUEwMDUwNjMxVE5MOVYyUzRZNUhMJmVuY3J5cHRlZEFkSWQ9QTAyMTc1NDZRQVJERDNEQzgxM1Mmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl)
-   Optional - [Protective case for Pico](https://www.amazon.com/C4Labs-Zebra-Pico-Case-Raspberry/dp/B08X24QJZC/ref=sr_1_3?crid=3L7RQXKD6KT72&keywords=pi+pico+case&qid=1679515852&s=electronics&sprefix=pi+pico+case%2Celectronics%2C108&sr=1-3)
-   Optional - [PoE to USB Power Supply](https://www.sparkfun.com/products/18709)
-   Wi-fi network with login credentials
-   PC to connect to Pi Pico
-   USB A to Micro-B cable (included with Pico link above, works with PoE)
-   Zabbix server (virtual or bare metal)

### Software

-   Text editor such as [Thonny](https://thonny.org/) or [VS Code](https://code.visualstudio.com/download)
-   Latest [UF2 firmware for Pi Pico W](https://rpf.io/pico-w-firmware) (click to download) or install via [MicroPython](https://micropython.org/download/rp2-pico-w/) or [Raspberry Pi](https://www.raspberrypi.org/) website
-   [Zabbix 5.x or 6.x](https://www.zabbix.com/)

Note: Thonny text editor is beginner friendly while VS Code is a more advanced option.

---

## Getting Started

There will be two separate sections for getting started:

1. _Quick Start Guide_ - Get a Pico sensor up and running as quick as possible. This guide will use Thonny text editor.
2. _Full Guide_ - Code walkthrough, setting up a Zabbix server with a Raspberry Pi 4, enclosing Pi Pico with a case. This version will use VS Code.

### Quick Start Guide

To begin you will need all hardware and software, except for the case and PoE to USB power supply, from the _Requirements_ section above. If you do not want to use a Zabbix server then you can still get the sensor working in the Pico console. You are, of course, welcome to modify the code to fit your needs.

If you purchased the Pico from the link above you are good to go. If you do not have headers soldered then make sure you get that done before moving on. Let's begin!

1.  Take the Pico and the USB A to Micro-B cable, plug the Micro-B (small) side into the Pico. Do not plug in to the PC yet.

    ![Pico-Micro-B Plug](https://github.com/prwilliams5/pico_sensor/blob/main/images/pico-top-plug.png)

2.  Hold the BOOTSEL button, circled in red below, on the Pico and plug the cable into the PC simultaneously.

![BOOTSEL Button](https://github.com/prwilliams5/pico_sensor/blob/main/images/bootsel.png)

3.  Your file manager should open automatically and show the Pico as a connected external drive. If your file manager does not open then see the help directly below.

    -   Windows - Go to your desktop and press the _Windows_ key + the _E_ key simultaneously or search for _File Explorer_ in Windows search. This will bring up a window that looks similar to below and the Pico will show up near the red circle.

        ![Windows File Explorer](https://github.com/prwilliams5/pico_sensor/blob/main/images/windows-file-explorer.png)

    -   MacOS - Press the _Command_ key plus the _Spacebar_ simultaneously and search for _Finder_. This will bring up a window similar to below, the Pico will show up near the red circle.

        ![MacOS Finder](https://github.com/prwilliams5/pico_sensor/blob/main/images/macos-finder-example.png)

    Now drag and drop the UF2 firmware file you downloaded into the Pico in the _File Explorer_ or _Finder_ app in your respective operating system.

4.  Open Thonny text editor and look at the bottom right corner of the the window. It should look similar to this when you click on it.

    ![Thonny Python Interpreter](https://github.com/prwilliams5/pico_sensor/blob/main/images/thonny-interpreter-example.png)

    If The _MicroPython (Raspberry Pi Pico)_ option is not selected then click on it to select.

5.  Now that we have the Pico connected to Thonny you should see a window with two sections that looks similar to below.

    ![Full Thonny Example](https://github.com/prwilliams5/pico_sensor/blob/main/images/full-thonny-example.png)

    In the bottom section under _Shell_ click to the right of the ">>>" prompt. You should be able to input some code and get some output in this shell terminal. Type or copy/paste the code below after clicking.

    `print('Hello World!')`

    This will output _Hello World_ to the shell terminal. This means the Pico is ready for the next steps.

6.  Click on the following link for the main.py file of this repository and copy all of the code in the code block. It starts with "import network" and ends with "main()". https://github.com/prwilliams5/pico_sensor/blob/main/main.py

7.  In Thonny editor paste the code block into the top section just under _untitled_, you will paste starting on the line with the number 1. It will look similar to this.

    ![Thonny Example](https://github.com/prwilliams5/pico_sensor/blob/main/images/thonny-example.png)

    We do need to modify the script a bit to get this working for you environment. Use the following steps.

    -

    Now click the _save_ icon in the toolbar above _untitled_ and select _Save to Pico_. Make sure to name the file main.py or the script will not run automatically when plugged in to power with no PC.

8.  Now, the wires for the DHT22 and water sensors need to be connected to specific header pins so the Pico can read the sensor data and send it to the Thonny shell/console for testing, then eventually Zabbix.

    In order to wire the pins correctly it is a good idea to pull up the [Raspberry Pi Pico Datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf). This will help determine where to plug the _Power_, _Ground_, and _Data_ wires from each sensor.

---

**This project is a work in progress and will continue to be updated.**
