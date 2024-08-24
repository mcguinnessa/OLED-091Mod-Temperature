#!/bin/python3

import time
import signal
import sys
import requests
import getopt

from oled_updater import OledUpdater

DEFAULT_INTERVAL = 60

class Daemon:
   def __init__(self, ds18b20_host, ds18b20_port, dht11_host, dht11_port, interval=DEFAULT_INTERVAL):
      self.interval = interval
      self.running = True

      self.ds18b20_host=ds18b20_host
      self.ds18b20_port=ds18b20_port
      self.dht11_host=dht11_host
      self.dht11_port=dht11_port

      self.oled = OledUpdater()

   def start(self):
      # Set up signal handlers for graceful termination
      signal.signal(signal.SIGTERM, self.stop)
      signal.signal(signal.SIGINT, self.stop)

      while self.running:
         ft_temp = self.get_ft_temp()
         room_temp = self.get_room_temp()
         self.oled.update_display(ft_temp, room_temp)

         print("Sleeping for " + str(self.interval) + "s")
         time.sleep(self.interval)

   def stop(self, signum, frame):
      print("OLED Daemon is stopping...")
      self.running = False

   def get_ft_temp(self):
      ft_resp = requests.get("http://" + self.ds18b20_host + ":"+self.ds18b20_port + "/DS18B20/c")
      #ft_resp = requests.get("http://192.168.0.126:5000/DS18B20/c")
      ft_temp = "Err"
      if ft_resp.status_code == 200:
         ft_json_data = ft_resp.json()
         ft_temp = "%.1f" % ft_json_data['value']
         print("FT Temp:" + str(ft_temp))

      return ft_temp

   def get_room_temp(self):
      room_temp = "Err"
      #room_resp = requests.get("http://192.168.0.126:5001/DHT11/c")
      room_resp = requests.get("http://"+ dht11_host+":"+ dht11_port +"/DHT11/c")
      if room_resp.status_code == 200:
         r_json_data = room_resp.json()
         #print("ROOM:" + str(r_json_data))
         room_temp = "%.0f" % r_json_data['value']
         print("ROOM Temp:" + str(room_temp))
      return room_temp 

if __name__ == "__main__":


#   try:
#   except getopt.GetoptError:
#      print('<oled_temperature_daemon.py -i>')
#      sys.exit(2)

   try:
      opts, args = getopt.getopt(sys.argv[1:],"i:a:b:c:d:",["interval=", "--ds18b20_host", "--ds18b20_port", "--dht11_host", "--dht11_port"])
      #opts, args = getopt.getopt(argv, "li:f:", ["log="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   interval = DEFAULT_INTERVAL
   ds18b20_host=""
   ds18b20_port=""
   dht11_host=""
   dht11_port=""

   for opt, arg in opts:
      if opt == '-h':
         print('<oled_temperature_daemon.py -i>')
         sys.exit()
      elif opt in ("-i", "--interval"):
         print("OPT:" + str(arg))
         interval=int(arg)
      elif opt in ("-a", "--ds18b20_host"):
         print("OPT:" + str(arg))
         ds18b20_host=str(arg)
      elif opt in ("-b", "--ds18b20_port"):
         print("OPT:" + str(arg))
         ds18b20_port=str(arg)
      elif opt in ("-c", "--dht11_host"):
         print("OPT:" + str(arg))
         dht11_host=str(arg)
      elif opt in ("-d", "--dht11_port"):
         print("OPT:" + str(arg))
         dht11_port=str(arg)

   try:  
      daemon = Daemon(ds18b20_host, ds18b20_port, dht11_host, dht11_port, interval=interval)
      print("OLED Daemon is starting...")
      daemon.start()
      print("OLED Daemon has stopped.")
   except Exception as e:
      print("OLED Daemon failed due to " + str(e))
