# The goal of this script is to get all the stats from the sensors to:
# - print to the epaper screen
# - print to plant_stats.csv - you can then use a spreadsheet of choice and draw cool graphs from it.
# - Drive the different microcontrolers to control inside climate: turn on/off fans, heat mat (not done), and water the plan if needed.
# (this last one does overlap with the auto_water.py... you choose which one to use)
# I put it in crontab to start a reboot
# $ sudo crontab -l
# @reboot cd /home/pi/Documents/SpaceBucket/FlaskWateringServer/; python3 print_status_epaper.py

import water
import epaper
import datetime
import time
import RPi.GPIO as GPIO

if __name__ == "__main__":
    
    # To use on the while loop
    booleankey = True

    PUMP_PIN=38 # To relay channel IN1
    IN2_PIN=36 # for fans
    IN3_PIN=32 # available... potentially heat mat
    IN4_PIN=37 # for lights

    # Variables used to control refresh and automation 
    delaytime = 600
    temp_low_limit = 20.0
    temp_high_limit = 25.0
    hum_low_limit = 50.0
    hum_high_limit = 75.0
    dry_days_limit = 4
    soil_moist_low_limit = 25
    
    while (booleankey):
        try:
            string[0] = "{}".format(datetime.datetime.now().strftime("%a %d %b %Y %I:%M%p"))

            soil_status = water.get_status()
            soil_moist_percent = water.get_soil_moist_percent()
            days_since_watered = water.get_days_since_watered()
            temp, temp_F, hum = water.get_tuple_temp_hum()

            if (soil_status == 1):
                string[1] = "Soil is DRY!"

            else:
                string[1] = "Soil is WET"

            string[2] = "{0:0.1f} days since water".format(days_since_watered)
            string[3] = "Soil Moisture: {0:0.1f}%".format(soil_moist_percent)
            string[4] = "Temp: {0:0.1f}*C/{1:0.1f}*F".format(temp,temp_F)
            string[5] = "Humidity: {0:0.1f}%".format(hum)

            #print all 4 lines to epaper
            epaper.write_epaper(string[0],string[1],string[2],string[3],string[4],string[5])


            #print to stats to .csv file as well (timestamp, temp, tempF, hum, soilmoisture, fan on?, light on?, days since watered)
            is_fan_on= water.check_gpio_status(IN2_PIN)
            is_light_on=water.check_gpio_status(IN4_PIN)

            now_isoformat = datetime.datetime.now().isoformat()

            # Decided to put the stats file in ./static to be able to easily access it via a web browser
            f = open('./static/plant_stats.csv', "a")
            f.write("{0},{1:0.1f},{2:0.1f},{3:0.1f},{4:0.1f},{5},{6},{7}\n".format(now_isoformat,temp,temp_F,hum,soil_moist_percent,is_fan_on,is_light_on,days_since_watered))
            f.close()

            # Low temperature, low RH, then turn fans off
            if (temp < temp_low_limit or hum < hum_low_limit):
                water.fans_off()
            # high temperature, high humidity, then turn fans on
            elif (temp > temp_high_limit or hum > hum_high_limit):
                water.fans_on()

            # If soil moisture is too low (dry), then turn on pump for default 5min
            if (days_since_watered > dry_days_limit):
                water.pump_on_demand()

            elif (soil_moist_percent < soil_moist_low_limit):
                water.pump_on_demand()

            time.sleep(delaytime)


        except KeyboardInterrupt:
            booleankey = False
