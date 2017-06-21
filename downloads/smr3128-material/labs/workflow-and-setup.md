**Workflow**: Setting up the development Environment and programming workflow

# Workflow & Setup

## Upgrading Lopy firmware
Pycom devices firmware is constantly improving so this is highly recommended to upgrade the firmware regularly: https://docs.pycom.io/pycom_esp32/pycom_esp32/getstarted.html#firmware-upgrades

The firmware includes among others, the micro Python libraries and modules ported specifically for the ESP32 microcontroller.

To upgrade the firmware, the procedure is the following:
1. first install the firmware upgrader tool available under the `softs/` folder (choose the one for your OS)
2. disconnect your device from your computer
3. connect a jumper cable or wire between G23 and GND (on the expansion board)
4. reconnect the board via USB to your computer
5. run the Firmware Upgrade tool (select your driver)
6. remove the G23 to GND jumper cable/wire
7. reboot the device (button or power off then on)

Below a screenshot of the Firmware Upgrader in action:
![img/firmware-upgrader.png](http://i.imgur.com/BO7x0nd.png)


## Getting Pycom libraries
> For Pysense and Pytrack boards

This repository contains out of the box examples and Python utility `classes` for Pycom devices (including Pysense and Pytrack).

These libraries: https://github.com/pycom/pycom-libraries are shared on GitHub. 

To download them, there are several options (including downloading them as a `zip` archive) but the preferred way is to clone the repository locally. Then as this repository is frequently updated, we will just need to pull the repo. on a regular basis.

To clone a repository using GitHub Desktop:

**1. Copy the cloning url**

![img/github-cloning.png](http://i.imgur.com/DlC81dL.png)

**2. In GitHub Desktop**

In top menu ► File ► Clone Repository...

Paste the cloning url and specify the local path where you want to save it.

And clone it...

![img/github-desktop-cloning.png](http://i.imgur.com/LkM6asK.png)

On a regular basis, press the `fetch origin` button to get updated version:

![img/fetch-origin-pycom-lib.png](http://i.imgur.com/kZQduaM.png)

## Typical Lopy device workflow
A typical workflow is the following:

1. Open Atom
2. Add a project folder: `top menu ► File ► Add Project Folder...`
3. Plug your device into your USB port
4. Update Pymakr settings (connection via USB or WiFi)
5. Connect
6. Write your code
7. Run your code for debugging
8. Sync your code once done


Taking a look at the screenshot below you will notice that the Atom-Pymakr plugin console provides dedicated buttons for most of these tasks:

![img/pymkr-console.png](http://i.imgur.com/cenBljF.png)

### Updating Pymakr settings
You need to update Pymakr settings every time you want to connect to a new device or you want to change your connection mode (USB serial or WiFi).


* **Connect via USB serial**

See Pycom official documentation: https://docs.pycom.io/pycom_esp32/pycom_esp32/toolsandfeatures.html

To connect via USB serial you need to know to determine the serial address in which your Pycom device is connected, you will need to scan for connected devices on your computer.

For Mac user, you can simply run in a terminal the following command: `ls /dev/cu.*`

Alternatively, you can use directly the Pymakr console to get a list of devices: click on the `More` button and `Get Serial ports`.

Once identified your serial device you need to update Pymakr settings. In Pymakr console: 
`Settings ► Global settings`

![img/pymkr-settings-details.png](http://i.imgur.com/37CqqVq.png)

> Note in screenshot above that you can specify a subfolder of your Atom project containing your code (will be seen in lab sessions).

* **Connect via WiFi**
1. Simply connect your computer to device's WiFi:

![img/lopy-wifi.png](http://i.imgur.com/7GbsuFk.png)

2. Reset Pymakr settings to default (no usb device address)

And that's all.

## Resetting
They are different ways to reset your device:

1. Soft reset

`ctrl+D` in Pymarkr plugin console.

2. Formating device's `/flash` folder
```python
import os
os.mkfs('/flash')
```
then reboot.

## Fetching data from the Lopy with Filezilla

> Warning: Your device's WiFi should be in Acces Point mode.

To establish a connection with your device:

1. Connect to device's WiFi


![img/filezilla-settings.png](http://i.imgur.com/SAN02Pa.png)