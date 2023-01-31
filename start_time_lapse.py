# The goal of this script is to find the latest file number, and the call the time lapse function
# I put it in crontab to start a reboot.
# $ sudo crontab -l
# @reboot cd /path/to/project/; python3 start_time_lapse.py

import water
import psutil
import datetime
import os
import glob

delaytime = 900
max_number_picture_count = 2880

if __name__ == "__main__":
    # find latest file number or start at 1.jpg
    IMG_FOLDER = os.path.join('static', 'time-lapse')
    file_type = r'/*.jpg'
    files = glob.glob(IMG_FOLDER + file_type)
    try:
        latest_file = max(files, key=os.path.getctime)
        file_start = latest_file.split('.')
        next_file_path = file_start[0]
        next_file = next_file_path.split('/')
        next_file_num = int(next_file[2])+1
    except:
        next_file_num = 1
        
    # sleep for 15mins, and take a total of 2880 pics - around 30 days    
    water.take_time_lapse(next_file_num,delaytime,max_number_picture_count)