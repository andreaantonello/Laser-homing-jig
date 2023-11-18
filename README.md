# Laser homing jig testing tool
Repository to test the ACCURACY of the robot

## Background - Hardware
The [Panasonic HG-C1100-P laser sensor](https://www3.panasonic.biz/ac/ae/search_num/index.jsp?c=detail&part_no=HG-C1100-P) is being sampled with a 
[Picotech's Picolog 1216](https://www.picotech.com/data-logger/picolog-1000-series/multi-channel-daq) data logger.
Signal are routed to the logger with the aid of [Picotech's Terminal Board](https://www.picotech.com/data-logger/picolog-1000-series/multi-channel-daq).

## Picolog SDK
The first step is to install the drivers for the Picolog logger, which can be found 
at [this link](https://www.picotech.com/downloads/linux). This install is specific for Ubuntu 18.04 LTS.
From terminal, add the repository to the updater:
 										
    sudo bash -c 'echo "deb https://labs.picotech.com/debian/ picoscope main" >/etc/apt/sources.list.d/picoscope.list'

Then, import the public key and update package manager cache:

 										
    wget -O - https://labs.picotech.com/debian/dists/picoscope/Release.gpg.key | sudo apt-key add -
    sudo apt-get update

Install now PicoScope:
 										
    sudo apt-get install picoscope
				
Open a terminal window. Navigate to the the `/opt/picoscope` directory and install 
the drivers for Picolog 1216:

    cd /opt/picoscope
    sudo apt-get install libpl1000


In order to use the Picolog SDK for sampling the laser sensors analog voltage, 
Picotech's SDK link should be included in the Pipfile:

    picosdk = {git = "https://github.com/picotech/picosdk-python-wrappers",ref = "master",editable = true}

The SDK can then be called from the script with 

    from picosdk.pl1000 import pl1000 as pl

## Meter reading
In order to read values from the meters, the sampling class is called `SampleMeter()`. 
To get a sampled valued from the meter