# piStat
Updated version of my SSD1306 display for RPI stats.

**DON'T FORGET TO ADD wifi_secrets.h file into the folder, where your .cpp file is!**
Example of content for that file:
```
#define SECRET_SSID "network_ssid"
#define SECRET_PASS "network_password"
#define SECRET_APIL "https://your_website/api/stats"
#define SECRET_FLASK "127.0.0.0:5001"
```

Also make sure you're using 2.4GHz network, most ESP modules support only this freq.

# Wiring
For power supply I chose PD Type-C to 4 pin

<img src="https://ae-pic-a1.aliexpress-media.com/kf/Sf9f02b165a41477ea3889d6d626e3d47D.jpg_960x960q75.jpg_.avif">

WIP wiring diagram

<img src="https://github.com/MYCELIUM-GH/piStat/blob/b252f13e49a16a57c5bc7986bd0ce998a8e7a061/wiring.png">


# Additional

If you wish to create new daemon for autostarting this app - simply create new service like this:
`/etc/systemd/system/change_me.service`

It should look like this:

```ini
[Unit]
Description=change_me
After=network.target

[Service]
User=change_me

WorkingDirectory=/home/change_me_to_your_dir

# replace the path with the exact path to your venv's python executable
ExecStart=/home/change_me_to_your_dir/venv/bin/python /home/change_me_to_your_dir/stats.py

Restart=always

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
