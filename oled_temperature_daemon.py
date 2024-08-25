#!/bin/python3

import time
import signal
import sys
import requests
import getopt
import logging

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

         logging.debug("Sleeping for " + str(self.interval) + "s")
         time.sleep(self.interval)

   def stop(self, signum, frame):
      logging.info("OLED Daemon is stopping...")
      self.running = False

   def get_ft_temp(self):
      ft_resp = requests.get("http://" + self.ds18b20_host + ":"+self.ds18b20_port + "/DS18B20/c")
      #ft_resp = requests.get("http://192.168.0.126:5000/DS18B20/c")
      ft_temp = "Err"
      if ft_resp.status_code == 200:
         ft_json_data = ft_resp.json()
         ft_temp = "%.1f" % ft_json_data['value']
         logging.debug("FT Temp:" + str(ft_temp))

      return ft_temp

   def get_room_temp(self):
      room_temp = "Err"
      #room_resp = requests.get("http://192.168.0.126:5001/DHT11/c")
      room_resp = requests.get("http://"+ dht11_host+":"+ dht11_port +"/DHT11/c")
      if room_resp.status_code == 200:
         r_json_data = room_resp.json()
         #print("ROOM:" + str(r_json_data))
         room_temp = "%.0f" % r_json_data['value']
         logging.debug("ROOM Temp:" + str(room_temp))
      return room_temp 


def usage():
   print('<oled_temperature_daemon.py -i>')



#################################################################################################
#
# MAIN
#
#################################################################################################
if __name__ == "__main__":

   try:
      opts, args = getopt.getopt(sys.argv[1:],"i:a:b:c:d:l:",["interval=", "--ds18b20_host=", "--ds18b20_port=", "--dht11_host=", "--dht11_port=", "--loglevel="])
      #opts, args = getopt.getopt(argv, "li:f:", ["log="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   interval = DEFAULT_INTERVAL
   ds18b20_host=""
   ds18b20_port=""
   dht11_host=""
   dht11_port=""
   loglevel = "DEBUG"

   for opt, arg in opts:
      if opt == '-h':
         print('<oled_temperature_daemon.py -i>')
         sys.exit()
      elif opt in ("-i", "--interval"):
         interval=int(arg)
         print("Interval:" + str(interval))
      elif opt in ("-a", "--ds18b20_host"):
         ds18b20_host=str(arg)
         print("DS18B20 Host:" + str(ds18b20_host))
      elif opt in ("-b", "--ds18b20_port"):
         ds18b20_port=str(arg)
         print("DS18B20 Port:" + str(ds18b20_port))
      elif opt in ("-c", "--dht11_host"):
         dht11_host=str(arg)
         print("DHT11 Host:" + str(dht11_host))
      elif opt in ("-d", "--dht11_port"):
         dht11_port=str(arg)
         print("DHT11 Port:" + str(dht11_port))
      elif opt in ("-l", "--loglevel"):
         loglevel=str(arg)
         print("Log Level:" + str(loglevel))


   numeric_log_level = getattr(logging, loglevel, None)

#   logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='/var/log/film_manager/upload_from_files.log', filemode='w', level=logging.DEBUG)
#   logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='/var/log/fishtank/oled_daemon.log", filemode='w', level=logging.DEBUG)
   logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='./oled_daemon.log', filemode='w', level=logging.DEBUG)
   logging.getLogger("smbprotocol").setLevel(logging.ERROR)
   console = logging.StreamHandler()

   #console.setLevel(logging.INFO)
   console.setLevel(logging.DEBUG)

   formatter = logging.Formatter('%(levelname)-8s %(message)s')
   console.setFormatter(formatter)

   try:  
      daemon = Daemon(ds18b20_host, ds18b20_port, dht11_host, dht11_port, interval=interval)
      logging.info("OLED Daemon is starting...")
      daemon.start()
      logging.info("OLED Daemon has stopped.")
   except Exception as e:
      logging.info("OLED Daemon failed due to " + str(e))
