# dclutter
Declutter app for Raspberry Pi with Inky What

## For Raspberry pi, first clone the dclutter code

### 1. Install Drivers and dependencies

```
curl https://get.pimoroni.com/inky | bash
```

Install MQTT Libraries

```

pip install paho-mqtt
```

### 3. Clone the repository to home directory
```
git clone 
```

### 3. Install Service

```
sudo nano /lib/systemd/system/dclutter.service
```

Add content to the file 

```
[Unit]
Description=Declutter Service
After=multi-user.target
Requires=network.target
[Service]
Type=idle
User=pi
Restart=always
ExecStart=/usr/bin/python /home/pi/dclutter/app.py > /home/pi/dclutter/service.log 2>&1

[Install]
WantedBy=multi-user.target
```
Test the service by 

```
sudo systemctl start dclutter.service
```

Enable the service using

```
sudo systemctl enable dclutter.service
```



wget https://raw.githubusercontent.com/kaushleshchandel/dclutter/main/app.py
