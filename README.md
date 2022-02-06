# dclutter
Declutter app for Raspberry Pi with Inky What

## For Raspberry pi, first clone the dclutter code



Add this to startup to autoupdate the app.py file

#1. Crontab

Edit the crontab file

```
sudo crontab -e
```

Add to the end of file

@reboot python3 /home/pi/dclutter/app.py > /home/pi/dclutter/app.log 2>&1




wget https://raw.githubusercontent.com/kaushleshchandel/dclutter/main/app.py
