# IIoT_module6
IIoT Workshop - Module 6 
Case Study 1 Example Code

Steps in a short list:
1.	RPi board should have wifi function. Check your RPi board model using command:
  cat  /proc/cpuinfo
2.	Verify the system clock synchronization. System clock needs to be synchronized:
  timedatectl
3.	Check the python version. Requires python 3.7 version or above. Please note the double dash:
  python --version  
4.	Install or update setup tools for python:
  sudo pip3 install --upgrade setuptools
5.	In order to use CircuitPython, we need to install a library called adafruit_blinka. We can complete it by running the following script:
  sudo pip3 install --upgrade adafruit-python-shell

  wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py 
  
  sudo python3 raspi-blinka.py
  
it may take a while to complete the installation. Please be patient. Choose Y to Reboot Now after the installation.  
7.	install BME280 library using command: 
  sudo pip install adafruit-circuitpython-bme280 
8.	download example code and check if it works:
  wget https://raw.githubusercontent.com/JZ2211/IIoT_module5/ main/demo_bme280.py 
  
  wget https://raw.githubusercontent.com/JZ2211/IIoT_module5/ main/savedata_locally.py 
  
  python demo_bme280.py
  
9.	check if Flask is installed:  pip show flask
10.	if not, please install flask before continue: sudo apt install python3-flask
11.	install plotly and pandas (you may need to use pip3 if the Raspberry Pi OS is old): 
  pip install plotly (location: /home/pi/.local/lib/python3.9/site-packages)
  pip install pandas (location: /home/pi/.local/lib/python3.9/site-packages)
12.	If there is an error to import pandas: libf77blas.so.3: cannot open shared object file: No such file or directory. See reference at: https://numpy.org/devdocs/user/troubleshooting-importerror.html), run: 
  sudo apt-get install libatlas-base-dev 
13.	Download case1 package from github in the Raspberry Pi (assume to the home directory /home/pi/):
  git clone https://github.com/JZ2211/IIoT_Case1.git
14.	Please make sure IIoT_Case1 and sub-directories LocalSite and templates has the write permission for the user owner. If not, change the permission using chmod u+w.
15.	Obtain the IP address of the host using ifconfig or hostname -I, this will be used to access the web server.
16.	Check if the example code program works: 
 python IIoT_Case1/bme280_example.py
17.	Open another ssh terminal, run: 
  python IIoT_Case1/LocalSite/localsite.py
18.	If it works, setup crontab to run in the background. Run:
  crontab -e 
Add the following lines to the crontab file: 
  @reboot sleep 10 && python /home/pi/IIoT_Case1/bme280_example.py
  @reboot sleep 20 && python /home/pi/IIoT_Case1/LocalSite/localsite.py
  0 0 * * 0 sudo reboot
19.	Reboot the RPi and now you can access the site use the url: <ip-address>:5000/<sensorID> for the most recent data in plain text display or <ip-address>:5000/<sensorID>/plots. For example, 192.168.1.2:5000/sensor1  or 192.168.1.2:5000/sensor1/plots. 
