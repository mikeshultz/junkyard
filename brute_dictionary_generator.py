import sys, os, itertools, argparse

parser = argparse.ArgumentParser(description='Generate a brute force dictionary.')
parser.add_argument('--uppercase', '-C', dest='upper', action='store_true', default=False, help='Include upercase letters.')
parser.add_argument('--lowercase', '-c', dest='lower', action='store_true', default=True, help='Include lowercase letters.')
parser.add_argument('--digits', '-d', dest='digits', action='store_true', default=False, help='Include digits.')
parser.add_argument('--special', '-s', dest='special', action='store_true', default=False, help='Include special characters.')
parser.add_argument('--min', '-m', dest='min', type=int, default=3, help='Minimum characters in password.')
parser.add_argument('--max', '-M', dest='max', type=int, default=6, help='Maximum characters in password.')
parser.add_argument('--file', '-f', dest='outfile', type=str, nargs='?', help='Filename to write to. If not specified, stdout.')
parser.add_argument('--do-not-delete', dest='delete', action='store_false', help='DO NOT delete FILE, just append to it.')
args = parser.parse_args()

# Constants for character combinations
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
SPECIAL = '!@#$%^&*()_+-=/\\'

# Combine the constants into an overall pool of chars depending on options
pool = ''
if args.upper:
    pool += UPPER
if args.lower:
    pool += LOWER
if args.digits:
    pool += DIGITS
if args.special:
    pool += SPECIAL

# setup the file to append to(if applicable) and delete the previous one
if args.delete:
    if os.path.exists(args.outfile):
        os.remove(args.outfile)

if args.outfile:
    file_handler = open(args.outfile, "a")
else:
    file_handler = None

def generate_by_length(length):
    """ Generate passwords that are X long """
    products = itertools.product(pool, repeat=length)
    for i in products: 
        if file_handler:
            file_handler.write(''.join(i) + '\n')
        else:
            sys.stdout.write(''.join(i) + '\n')

# Generate the full range
x = args.min
while x <= args.max:
    generate_by_length(x)
    x += 1 

sys.exit(0)
