# Cisco-WLC-Site-Stats
This Python script queries the Cisco WLC and returns the connection statistics for currently connected clients

I requires the Netmiko, argparse, and re libraries.

This Python script will look through the AP names that contain the site ID that you specify at the command line.  This was written for a site that uses the naming scheme of SiteID-Floor-APName to name the access points so it looks for all instances of the AP name of the controller specified at runtime and then queries them to return the SNR, RSSI, and current speed rate for each MAC address connected to the access point.  It seperates the output by the 2.4 & 5 Ghz bands.

````
Command syntax: python wifi_site_stats.py -i <WLC IP Address> -s <Site ID or AP name> -u <username> -p <password>


Example Output: 

Use the channel widths on this chart to get the actual speed: http://mcsindex.com/

199-2W-AP04       Channel Width.............................. 80 Mhz
199-1W-AP03       Channel Width.............................. 20 Mhz
199-2W-AP08       Channel Width.............................. 80 Mhz
199-1W-AP05       Channel Width.............................. 20 Mhz
#####################         Clients on the 5ghz band:           #####################
      ********** 64:b0:a6:90:72:38**********
Current Rate..................................... m8 ss2
      Radio Signal Strength Indicator............ -45 dBm
      Signal to Noise Ratio...................... 43 dB
      ********** f8:a5:c5:9f:fd:92**********
Current Rate..................................... m8 ss1
      Radio Signal Strength Indicator............ -57 dBm
      Signal to Noise Ratio...................... 39 dB
      ********** ac:5f:3e:c3:46:0a**********
Current Rate..................................... m8 ss2
      Radio Signal Strength Indicator............ -66 dBm
      Signal to Noise Ratio...................... 30 dB
  ````
