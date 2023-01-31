# bluebucketpi

A Flask webapp that runs python code on a Raspberry Pi to control and monitor a growing plant... usually in a SpaceBucket (https://www.reddit.com/r/SpaceBuckets/), hence the name. But it could be adapted to other use cases.
The webapp will have the rPi take pictures (for time-lapses), read sensors (moisture, humidity, temperature), control fans, lights and water pump, and write data to a csv file as well as to an epaper display.
Starter idea and initial code forked from here: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc

## Hardware Materials:
- A Raspberry Pi (I used a 3B+ I had collecting dust - you might have to steal or beg for one in 2023), and a 32GB micro SD card.
- A 4channel relay (5volt for microcontrollers - used this one: https://www.amazon.com/dp/B08PP8HXVD)
- A capacitance moisture sensor (used the "v1.2" available online. Kit: https://www.amazon.com/dp/B07TLRYGT1) - Resistance ones corrode easily.
- An Analog-to-digital converter ADS1115 (for the rPi to read the capacitance moisture sensor. Like this one https://www.amazon.com/dp/B07VPFLSMX)
- A low voltage water pump (included in the kit above with the moisture sensor)
- DHT22 sensor (eg: https://www.amazon.com/dp/B073F472JL)
- 80mm computer fans (used 2 to create airflow: https://www.amazon.com/dp/B002YFSHPY)
- LED grow lights (used a stick-on LED strip light: https://www.amazon.com/gp/product/B00HSF65MC)
- rPi camera (eg: https://www.amazon.com/dp/B07KF7GWJL)
- A 2.7in Waveshare ePaper display (eg: https://www.amazon.com/dp/B07PKSZ3XK)
- Power strip and Power supplies (used some USB charger blocks, an some 12v power adapters - mainly on each for the rPi, fans, pump, lights - sensors can be powered from the GPIO pins
- An enclosure - used some clear Sterilite storage box and made holes for the wiring
- Hardware store 5ga buckets (About 4) - check https://www.reddit.com/r/SpaceBuckets/ for details on how to build one.


## Software Materials:
- Started with latest Raspbian fully loaded
- Python3, with pip3.. and these packages. YMMV:
 ```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev python3-pip
sudo apt-get install build-essential python3-smbus
sudo apt-get install python3-pil
sudo apt-get install ffmpeg
```
- DHT sensor and ADS1x15 packages:
```
sudo pip3 install RPi.GPIO
sudo pip3 install Adafruit_DHT
sudo pip3 install Adafruit-ADS1x15
```
- Flask package and psutil:
```
sudo pip3 install flask
sudo pip3 install psutil
```
- For Flask, you will also need a folder structure like:
```
/path/to/project/python_scripts_go_here.py
/path/to/project/templates/main.html
/path/to/project/static/ # for image files. Read the readme there for more details.
```
- ePaper: Waveshare lib and pic folder from their repo: 
```
git clone https://github.com/waveshare/e-Paper.git
```
- setup root crontab like this (starts webapp, starts the time-lapse picture-taking, starts the stats printing/monitoring, creates a time-lapse mp4 daily at 5am):
```
$ sudo crontab -e
@reboot cd /path/to/project/; python3 web_plants.py > stdout.log 2> stderr.log
@reboot cd /path/to/project/; python3 start_time_lapse.py
@reboot cd /path/to/project/; python3 print_status_epaper.py
0 5 * * * cd /path/to/project/static/time-lapse/; ffmpeg -f image2 -r 30 -i ./%05d.jpg -vcodec mpeg4 -vb 4M -y time-lapse.mp4
```

## Wiring

Check out [pinout.xyz](https://pinout.xyz/) for pin details. We will use BOARD (Broadcom) pin assignment, which is the sequential number just next to the pin (There is an exception for the DHT22 sensor that I called out in the code).

### Relay Pins

DHT sensor: 
 - Signal to 40 or GPIO21(in the code needs to be entered the BCM number: 21)
Soil moisture sensor: 
 - Signal plugs into the ADS1115at: A0
ADS1115: 
 - SCL-> 5 (SCL on rpi)
 - SDA -> 3 (SDA on rpi)


more TBD...

PUMP_PIN=38 # To relay channel IN1
IN2_PIN=36 # for fans
IN3_PIN=32 # available... potentially heat mat, not use yet.
IN4_PIN=37 # for lights




## Pics
[Gallery in imgur](https://imgur.com/gallery/pSPXdEN)
![Webapp look](https://imgur.com/jHOXhhz.png)
![Finished bucket](https://i.imgur.com/wbZTlzX.jpeg)
![ePaper close up](https://i.imgur.com/bZjFKMB.jpeg)
![Peek inside](https://i.imgur.com/DYzQEvk.jpeg)
