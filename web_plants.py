# This initiates and starts the Flask app. 
# Credits: Forked from https://gist.github.com/benrules2/c4f3db455f4f2dfbe7d5b825b0b4ee36
# Put a crontab to start the Flask webserver on reboot:
# $ sudo crontab -l
# @reboot cd /path/to/project/; python3 web_plants.py > stdout.log 2> stderr.log

from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os
import glob

#ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'img')
#IMG_FOLDER = 'time-lapse'
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
file_type = r'/*.jpg'
files = glob.glob(IMG_FOLDER + file_type)
latest_file = max(files, key=os.path.getctime)


TL_FOLDER = os.path.join('static', 'time-lapse')

def template(title = "BlueBucketPi", text = ""):
    now = datetime.datetime.now().strftime('%A %d %b %Y %H:%M:%S')
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    templateData = template()
    return render_template('main.html', **templateData, plant_image=latest_file)

@app.route("/last_watered")
def check_last_watered():
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    days_since_watered = water.get_days_since_watered()
    text_to_template = water.get_last_watered() + " - {0:0.1f} days since then.".format(days_since_watered)
    templateData = template(text = text_to_template)
    return render_template('main.html', **templateData, plant_image=latest_file)

@app.route("/sensor")
def action():
    
    status = water.get_status()
    soil_moist_percent = water.get_soil_moist_percent()
    message = ""
    if (status == 1):
        message = "Water me please! Soil is DRY. Soil moisture: {0:0.1f}%".format(soil_moist_percent)
    else:
        message = "I'm a happy plant. Soil is WET. Soil moisture: {0:0.1f}%".format(soil_moist_percent)
        
    temp_humidity = water.get_temp_humidity()
    days_since_watered = water.get_days_since_watered()
    days_since_watered_text = " - {0:0.1f} days since watered.".format(days_since_watered)
    message = message + " - " + temp_humidity + days_since_watered_text
    
    # Need to put a cronjob to clean this img folder as it can grow with each click
    img_name ='{}/img-{}.jpg'.format(IMG_FOLDER,datetime.datetime.now().isoformat())
    #img_name ='{}/latest.jpg'.format(IMG_FOLDER) # Looked better/more efficient, but web browsers will cache the img and not refresh
    try:
        water.take_picture(img_name)
    except:
        message = message + " - Camera capture failed."

    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
       
    templateData = template(text = message)
    return render_template('main.html', **templateData, plant_image=latest_file)

@app.route("/water")
def action2():
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    templateData = template(text = "Watering Now...")
    render_template('main.html', **templateData)
    water.pump_on_demand()
    templateData = template(text = "Watered Once Completed!")
    return render_template('main.html', **templateData, plant_image=latest_file)

@app.route("/grow")
def action3():

    
    try:
        
        f = open("next_grow_pic.txt", "r")
        next_file_num = int(f.readline())
        next_file_name = TL_FOLDER + '/' + str(next_file_num) + '.jpg'
        f.close()
        next_file_num += 1

        # reset if the file is not there
        if not os.path.exists(next_file_name):
            next_file_num =1
            next_file_name = TL_FOLDER + '/' + str(next_file_num) + '.jpg'

        f = open("next_grow_pic.txt", "w")
        f.write(str(next_file_num))
        f.close()

    except:
        templateData = template(text = "Watch me grow is not working :( First file: {}".format(next_file_name))
        return render_template('main.html', **templateData, plant_image=next_file_name)
    
    templateData = template(text = "Press Watch Me Grow! again for next frame. First file: {}".format(next_file_name))
    return render_template('main.html', **templateData, plant_image=next_file_name)


@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")
    
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    latest_file_fixed = '../../' + latest_file

    return render_template('main.html', **templateData, plant_image=latest_file_fixed)

@app.route("/fans/<toggle>")
def fans_toggle(toggle):
    if toggle == "ON":
        water.fans_on()
        templateData = template(text = "Fans Turned On")
    else:
        water.fans_off()
        templateData = template(text = "Fans Turned Off")
    
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    latest_file_fixed = '../' + latest_file

    return render_template('main.html', **templateData, plant_image=latest_file_fixed)

@app.route("/lights/<toggle>")
def lights_toggle(toggle):
    if toggle == "ON":
        water.lights_on()
        templateData = template(text = "Lights Turned On")
    else:
        water.lights_off()
        templateData = template(text = "Lights Turned Off")
        
    files = glob.glob(IMG_FOLDER + file_type)
    latest_file = max(files, key=os.path.getctime)
    latest_file_fixed = '../' + latest_file

    return render_template('main.html', **templateData, plant_image=latest_file_fixed)

if __name__ == "__main__":
    try:
        # Start the basics: Fans and lights
        water.fans_on()
        water.lights_on()

        # Star the webapp
        # choose one app.run() and disable the rest                   
        
        #app.run(host='0.0.0.0', debug=True, ssl_context='adhoc') # This a quick and dirty HTTPS/SSL on port 5000
        #context = ('./certificates/server.crt', './certificates/server.key') # Sets context to your SSL certificates needed for below app.run()
        #app.run(host='0.0.0.0', port=4420, debug=True, ssl_context=context) # This sets HTTPS/SSL on port 4420 :) using your own certs above
        app.run(host='0.0.0.0', port=80, debug=True)   # Plain old HTTP on port 80 good enough for internal/safe network
    except KeyboardInterrupt:
        os.system ("pkill -f water.py")
        water.destroy()
