#!/bin/env python
"""
Adjust the brightness of your laptop's backlight.  Good for use with Fluxbox

Usage:

    /usr/bin/brightness.py --step 100 down /sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight

Fluxbox config `~/.fluxbox/keys`:

    232 :Exec /usr/bin/brightness.py --step 100 down /sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight
    233 :Exec /usr/bin/brightness.py --step 100 up /sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight
"""
import os
import sys
from pathlib import Path
from argparse import ArgumentParser

MAX_STEP = 1000
UNEXPECTED_STRUCTURE_ERROR = ValueError('Unexpected proc structure')

def get_file_contents(f):
    """ Read the text file f's' contents """
    if not f.is_file():
        raise UNEXPECTED_STRUCTURE_ERROR

    return f.read_text()

def write_file(f, v):
    """ Rewrite the file f with v """
    if not f.is_file():
        raise UNEXPECTED_STRUCTURE_ERROR

    return f.write_text(v)

def get_max_brightness(procdir):
    """ Get the max brightness supported """
    max_file = procdir.joinpath('max_brightness')
    return int(get_file_contents(max_file))

def get_brightness(procdir):
    """ Get the curent brightness """
    b_file = procdir.joinpath('brightness')
    return int(get_file_contents(b_file))

def set_brightness(procdir, val):
    """ Get the brightness to val """
    b_file = procdir.joinpath('brightness')
    return write_file(b_file, str(val))

def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument('command', metavar='COMMAND', nargs=1,
                    help='Command [up/down]')
    parser.add_argument('procdir', metavar='BRIGHTNESS_PROC', nargs='?',
                    help='Path to proc directory for backlight')
    parser.add_argument('--step', type=int, default=100,
                    help='Brightness value step (defualt: 100)')
    return parser.parse_args(argv)

def main(argv=sys.argv[1:]):
    args = parse_args(argv)

    if not args.procdir:
        args.procdir = os.environ.get('BRIGHTNESS_PROC')

        if not args.procdir:
            raise FileNotFoundError('Unable to find BRIGHTNESS_PROC')

    procdir = None

    if len(args.procdir) > 0:
        procdir = Path(args.procdir)

    if not procdir or not procdir.is_dir():
        raise ValueError('BRIGHTNESS_PROC is not a directory: {}'.format(procdir))

    if args.step < 0 or args.step > MAX_STEP:
        raise ValueError('Step must be between 0 and {}'.format(MAX_STEP))

    max_brightness = get_max_brightness(procdir)
    current = get_brightness(procdir)

    command = args.command[0]

    if command == 'up':
        next_brightness = current + args.step

        if next_brightness >= max_brightness:
            if current < max_brightness:
                next_brightness = max_brightness
            else:
                print('Already max brightness', file=sys.stderr)
                sys.exit(0)
    elif command == 'down':
        next_brightness = current - args.step

        if next_brightness <= 0:
            if current > 0:
                next_brightness = 0
            else:
                print('Already min brightness', file=sys.stderr)
                sys.exit(0)
    else:
        raise ValueError('Unknown command {}'.format(args.command))

    print('Setting brightness to {}'.format(next_brightness))
    set_brightness(procdir, next_brightness)
    sys.exit(0)

if __name__ == "__main__":
    main()
