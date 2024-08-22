#!/bin/python3

import time
import signal
import sys
import requests

from oled_updater import OledUpdater

INTERVAL = 60

class Daemon:
   def __init__(self, interval=INTERVAL):
      self.interval = interval
      self.running = True

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
      ft_resp = requests.get("http://192.168.0.126:5000/DS18B20/c")
      ft_temp = "Err"
      if ft_resp.status_code == 200:
         ft_json_data = ft_resp.json()
         ft_temp = "%.1f" % ft_json_data['value']
         print("FT Temp:" + str(ft_temp))

      return ft_temp


   def get_room_temp(self):
      room_temp = "Err"
      room_resp = requests.get("http://192.168.0.126:5001/DHT11/c")
      if room_resp.status_code == 200:
         r_json_data = room_resp.json()
         #print("ROOM:" + str(r_json_data))
         room_temp = "%.0f" % r_json_data['value']
         print("ROOM Temp:" + str(room_temp))
      return room_temp 

if __name__ == "__main__":
    daemon = Daemon(interval=INTERVAL)
    print("OLED Daemon is starting...")
    daemon.start()
    print("OLED Daemon has stopped.")
