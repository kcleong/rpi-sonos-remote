RPi Remote control for Sonos
============================

This script can be used to control a Sonos device using a remote 
control on a Raspberry Pi with an IR receiver. The RPi must be 
connected to the same network as a Sonos device or bridge.

The LIRC daemon is used the read infrared signals from 
the remote. The key which was pressed is read, and the action (such as 
volume up or down) is sent to the Sonos speakers. The Python library 
`SoCo`_ is used to control the speakers. 

.. _`SoCo`: https://github.com/SoCo/SoCo

Install
-------
Install LIRC and record ir codes from your remote using this tutorial:

    http://ozzmaker.com/2013/10/24/how-to-control-the-gpio-on-a-raspberry-pi-with-an-ir-remote/
    
Modify lircrc config in lircrc.example and save it to ~/.lircrc

Install required modules::

    sudo pip install -r requirements 

Run the remote receiver by running::

    python remote.py

To start the remote receiver on boot, add the following line to crontab::

    @reboot <path to script>/remote.py
