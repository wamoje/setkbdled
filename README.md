Utility to set colour and brightness of keyboard backlight led's.
Developed on a System76 Gazelle, but probably suited for all System76 laptops.

Last used values will be stored in /etc/kbdled.cfg. When called without
arguments, the values in this file will be used to set brightness and colour.

Arguments:
-c, --color, --colour:
    000000 - FFFFFF Six hexadecimal digits, upper or lowercase,
    two digits red, two digit green and two digit blue.
    Predefined values:
    -c red : gives FF0000
    -c green :     00FF00
    -c blue :      0000FF
    -c white :     FFFFFF
    -c purple :    FF00FF
    Colour values can be given in upper- or lowercase.
-b, --brightness:
    an integer from 0 to 255 (inclusive).

Pop!OS's systemd mechanism is (ab)used to set the led's during startup.
setkbled.service must be placed in /etc/systemd/system and give it the
permission bits 644 (chmod).
setkbled.py must be placed in /usr/local/bin, permission bits 744.
It is assumed that python3 is used and is present at /usr/bin/python3. If
this is different, please alter setkbled.service to represent the location
of python.

When all is in place you should run the commands:
sudo systemctl daemon-reload
sudo systemctl enable setkbled.service
Then the led's will be set on every restart.

You can set the values by editting /etc/kbled.cfg (not advised).
But the better way is:
sudo /usr/bin/python3 /usr/local/bin/setkbled.py -c 2200FF -b 48
These values will be activated and stored in /etc/kbled.cfg, so the settings
will be used again for the next restart.
