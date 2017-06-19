lora_gps

This example uses:
- a unit that transmits messages with the protocol lora
- a unit that receives messages lora and receives the gps position by connecting via wifi to an android app
The received gps data string is in json format and is transformed into a json array.

On the android smartphone you need:
1. Install the Share GPS app
	https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS&hl=en
	Share GPS
	Jillybunch Tools
	Share GPS supports the following major activities
	* Use your mobile as an external GPS for laptops/tablets that don't have GPS.
	* Share and update location real-time to a remote person using Google Earth or other KML compatible program
	* Save locations visited and share later with images and links with KML
	* Save tracks during activities such as driving, biking, and walking and share via KML files

	Share NMEA GPS sentences or act as a GPSD compatible server via the following methods:
	* Bluetooth
	* TCP/IP (wifi/mobile data)
	* USB 

	Share KML files via the following methods:
	* Dropbox
	* Google Drive
	* SSH/SCP
	* Local phone storage
	* Provider application

	Share GPS is an application for real-time location data sharing via a variety of methods. 
	It also supports saving tracks via KML/KMZ, allowing the user to record footprints while the app is running in the background. 
	Share GPS supports sending standard NMEA data over Bluetooth, USB, and TCP/IP.
	
2. Enable internet tethering.
    If no hotspot was created, create one with these parameters:
    Name "mrandroid", pass "eatmenow"
3. Launch the Share GPS app and follow these steps:
4. In connections press on the "test" connection and enable "listening"
5. Go to Gps Status and press the "Start Track" button

Note:
For tethering on android nexus smartphones, open the Settings app
Slide the hidden menu from left to right to open Settings Home
Press ... more
At the bottom there is Tethering & Portable Hotspot
Open Tethering & Portable hotspot
Portable wifi hotspot set on

Caution:
In order to use two sockets (wifi and lora), you need:
1) open socket1
2) manage the socket1
3) close the socket1
4) open socket2
5) Manage the socket2
6) close the socket2
7) Enter a delay (time.sleep (0.3) currently 0.3 sec)

Files:

├── gpsrx1.py						source of main.py on rx node
├── gpstx1.py						source of main.py on tx node
├── log
│   ├── acq19700101000655.csv		example of csv acquisition file
│   ├── acq19700101003831.csv		example of csv acquisition file
│   ├── acq19700101005806.csv		example of csv acquisition file
│   ├── loragps_log_format.odt		csv file specifications (openoffice)
│   ├── loragps_log_format.pdf		csv file specifications (pdf)
│   └── rd.sh
├── lora_rx_node					sw for lora rx node
│   ├── boot.py						boot.py module to install
│   ├── gpsrx1.py
│   └── main.py						main.py module to install
├── lora_tx_node					sw for lora tx node
│   ├── boot.py						boot.py module to install
│   ├── gpstx1.py
│   └── main.py						main.py module to install
├── readme_lora_gps.txt
└── utility							bash utilities to connect pycom boards
    ├── cpy.sh						write a .py file to pycom
    ├── cr.sh						write a .py file and execute rshell
    ├── rdpy.sh						read a .py file from pycom
    ├── rd.sh						read a file from pycom
    └── rs.sh						launch rshell



