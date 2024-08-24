# OLED-091Mod-Temperature
Daemon for displaying the temperature on a 0.91 LED display


#Create Service
create link to service file in /etc/systemd/system/OLED-091Mod-Temperature.service

sudo systemctl daemon-reload
sudo systemctl start OLED-091Mod-Temperature
sudo systemctl enable OLED-091Mod-Temperature
sudo systemctl status OLED-091Mod-Temperature
