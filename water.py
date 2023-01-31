# Main script... where all the magic happens.
import RPi.GPIO as GPIO
import datetime
import time
import Adafruit_ADS1x15
import math
import Adafruit_DHT
from picamera import PiCamera

#imports for e-paper
import logging

# TODO... not really logging anything yet.
logging.basicConfig(level=logging.INFO)


# Initializing and setting the ADS1115 analog-to-digital converter for the Soil Moisture sensor
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# We will use GPIO BOARD (Broadcom) pin assignment. Useful to use a breadboard with expansion board for easy access.
# Check https//pinout.xyz for location on pin numbers.
PUMP_PIN=38 # To relay channel IN1
IN2_PIN=36 # for fans
IN3_PIN=32 # available... potentially heat mat, not use yet.
IN4_PIN=37 # for lights

# For the DHT22 hygrometer sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_GPIOPIN = 21 # WARNING: this is GPIO BCM number not BOARD PIN number, which is BOARD PIN 40, for some reason... don't ask, please tell.

values = [0]*100

GPIO.setmode(GPIO.BOARD) # Setting to Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"

def get_days_since_watered():
    try:
        f = open("last_watered.txt", "r")
        last_watered = f.readline()
        f.close()

        # Calculate difference between to datetime objects, get the amount in seconds, and divide it by 86400 to get number in days
        # TODO: There might be a simpler way to get the now datetime object
        dt_object_now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
        dt_object_lw = datetime.datetime.strptime(last_watered[13:-1], '%A %d %b %Y %H:%M:%S')
        days_since_watered =  dt_object_now - dt_object_lw 
        days_since_watered = round ((days_since_watered.total_seconds())/86400,2)

        return days_since_watered
    except:
        return -1

# Moisture Sensor get status
def get_status():
    for i in range(100):
        values[i] = adc.read_adc(0, gain=GAIN)
    #print(max(values))
    
    if (max(values))>18000: # moisture sensor v1.2 enter 21000, sensor v2.0 enter 18000
        return 1  
    else:
        return 0

# Implementation of the Arduino map() function
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def get_soil_moist_percent():

    for i in range(100):
        values[i] = adc.read_adc(0, gain=GAIN)
    soil_moist_value = max(values)
    soil_moist_percent = _map (soil_moist_value,20000,8430,0,100)
    return soil_moist_percent
    
def get_temp_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_GPIOPIN)
    if humidity is not None and temperature is not None:
        temperature_F =  (temperature * 9/5) + 32
        message = "Temp:{0:0.1f}*C/{1:0.1f}*F Humidity:{2:0.1f}%".format(temperature,temperature_F,humidity)
    else:
        message = "Failed to retrieve data from DHT22 humidity sensor 2"
    return message

def get_tuple_temp_hum():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_GPIOPIN)
    if humidity is None and temperature is None:
        humidity = 0
        temperature = 0 
    temperature_F =  (temperature * 9/5) + 32
    return temperature,temperature_F,humidity;


def take_picture(img_name):
    camera = PiCamera()
    camera.rotation = 180
    timeinbetween = 2
    camera.resolution = (1024, 768)
    camera.annotate_text_size = 50 # (values 6 to 160, default is 32)
    camera.annotate_text = datetime.datetime.now().strftime('%A %d %b %Y %H:%M')
    camera.capture(img_name)
    camera.close()
    
def take_time_lapse(file_number,timeinbetween,consecutive_pics):
    counter = 0

    print("Starting Time Lapse pictures! Press CTRL+C to exit")
    try:
        while counter < consecutive_pics:
            n = '%05d' % file_number
            img_name = 'static/time-lapse/{}.jpg'.format(n)
            take_picture(img_name)
            print('Saved pic {} waiting {} minutes for the next pic.'.format(n, timeinbetween/60))
            time.sleep(timeinbetween)
            counter +=1
            file_number +=1
    except KeyboardInterrupt:
        camera.close()        

# setup the pin to drive the relays
def init_output(pin):
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    
def auto_water(delay = 1):
    consecutive_water_count = 0
    init_output(PUMP_PIN)
    print("Here we go! Press CTRL+C to exit")
    try:
        while consecutive_water_count < 10:
            time.sleep(delay)
            wet = get_status() == 0
            if not wet:
                print("Dry - turning pump on")
                #if consecutive_water_count < 5:
                pump_on()
                consecutive_water_count += 1
                if consecutive_water_count == 10:
                    print("Sleeping for 10mins")
                    pump_off()
                    time.sleep(600)
                    consecutive_water_count = 0
                    
            else:
                consecutive_water_count = 0
                pump_off()
        destroy() #exiting cleanly after all watering tries - this might never execute if we sleep/reset counter
        
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        destroy()

def destroy():
    GPIO.cleanup() # cleanup all GPIO

def pump_on():
    #init_output(PUMP_PIN) # Not needed as auto_water does do init_output(PUMP_PIN)
    f = open("last_watered.txt", "w")
    f.write("Last watered {}".format(datetime.datetime.now().strftime('%A %d %b %Y %H:%M:%S')))
    f.close()
    GPIO.output(PUMP_PIN, GPIO.HIGH)

    print("Dry - Pump ON")

def pump_off():
    #init_output(PUMP_PIN) # Not needed as auto_water does do init_output(PUMP_PIN)
    GPIO.output(PUMP_PIN, GPIO.LOW)

def pump_on_demand(delay = 300):
    init_output(PUMP_PIN)
    
    f = open("last_watered.txt", "w")
    f.write("Last watered {}".format(datetime.datetime.now().strftime('%A %d %b %Y %H:%M:%S')))
    f.close()
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    print("On Demand - Pump ON")
    time.sleep(delay)
    GPIO.output(PUMP_PIN, GPIO.LOW)
    
def fans_on():
    init_output(IN2_PIN)
    GPIO.output(IN2_PIN, GPIO.HIGH)

def fans_off():
    init_output(IN2_PIN)
    GPIO.output(IN2_PIN, GPIO.LOW)
    
def lights_on():
    init_output(IN4_PIN)
    GPIO.output(IN4_PIN, GPIO.HIGH)

def lights_off():
    init_output(IN4_PIN)
    GPIO.output(IN4_PIN, GPIO.LOW)
    
def check_gpio_status(pin):
    GPIO.setup(pin, GPIO.OUT)
    state = GPIO.input(pin)
    return state

