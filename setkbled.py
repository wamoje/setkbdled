#!/usr/bin/env python3
''' setkbled.py - Program to control keyboard background light

    Design considerations:
    - Make executable: shebang with env?
    - Runs during system startup (init.d or systemd?)
    - Without args: gets state from /etc, activates that state and
        prints the values used.
    - With args: Adjust lighting and save state in /etc
    - Research possibilities to make chosen state personal per user:
      save state in home-dir
      Run during login (gui)
    - Args:
      -h, --help: show usage, also shown in case of arg error
      -c, --colour, --color: Colour of keyboard leds
          '000FFF' RGB in hex or
          white, green, red, blue, purple
          colour attributes can be in upper- or lowercase
      -b, --brightness: 0-255

    Example: setkbled.py -c RED -b 127
'''

import argparse
import string
import sys
import os

COL = "FFFFFF"  # Set global colour to default
BRI = 64       # Set global brightness to default
CFG = '/etc/kbdled.cfg'

def main():
    parser = argparse.ArgumentParser(
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description='''\
        Set colour and brightness of the keyboard LED's.
        ================================================
        First the commandline arguments for colour and brightness will
        be interpreted, missing arguments will be read from /etc/kbdled.
        Colour and brightness of the LED's will be set and used values
        will be stored again in /etc/kbdled. So a next call without
        arguments will set again the last used values.
        The values of colour and brightness can be upper or lowercase:
        eg RED vs red and 00FFBB vs 00ffbb.
             ''')
    parser.add_argument('-c', '--colour', '--color',
                         help='Colour code in hex RGB or name of colour: '
                               'white, red, green, blue, purple.',
                         type=str)
    parser.add_argument('-b', '--brightness',
                        help='Brightness value from 0 to 255.',
                        type=int)
    args = parser.parse_args()
    get_values()
    if args.colour is not None:
        process_colour(args.colour)
    if args.brightness is not None:
        process_brightness(args.brightness)
    set_values()

def process_colour(colour):
    global COL
    colour = colour.upper()
    if colour == 'WHITE':
        colour = 'FFFFFF'
    if colour == 'RED':
        colour = 'FF0000'
    if colour == 'GREEN':
        colour = '00FF00'
    if colour == 'BLUE':
        colour = '0000FF'
    if colour == 'PURPLE':
        colour = 'FF00FF'
    if not checkhex(colour):
        print("Colour not correct, use --help to see options.")
        sys.exit(8)
    COL = colour

def process_brightness(brightness):
    global BRI
    if (
        (not isinstance(brightness, int))
        or (brightness < 0)
        or (brightness > 255)
       ):
        print("Brightness must be an integer between 0 and 255 (inclusive).")
        sys.exit(8)
    BRI = brightness

def get_values():
    global BRI
    global COL
    global CFG
    if os.path.exists(CFG):
        with open(CFG, 'r') as cfgf:
            config = cfgf.readlines()
        for line in config:
            if line.lower().startswith("colour"):
                colour = line.split(sep='=')[-1].strip().upper()
                if checkhex(colour):
                    COL = colour
            if line.lower().startswith("brightness"):
                brightness = line.split(sep='=')[-1].strip().upper()
                if brightness.isdigit():
                    brightness = int(brightness)
                    if brightness >= 0 and brightness <= 255:
                        BRI = brightness

def set_values():
    global BRI
    global COL
    global CFG
    with open(CFG, 'w') as cfgf:
        cfgf.write('brightness={}\n'.format(BRI))
        cfgf.write('colour={}\n'.format(COL))
    with open("/sys/class/leds/system76::kbd_backlight/color_left", "w") as kbcolor:
        kbcolor.write(COL)
    with open("/sys/class/leds/system76::kbd_backlight/brightness", "w") as kbbright:
        kbbright.write(str(BRI))
    print('Colour set to {}'.format(COL))
    print('Brightness set to {}'.format(BRI))

def checkhex(digits):
    hex = True
    for digit in digits:
        if digit not in string.hexdigits:
            hex = False
    return hex

if __name__ == "__main__":
    main()
