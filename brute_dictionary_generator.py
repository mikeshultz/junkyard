import sys, os, re, itertools, argparse

parser = argparse.ArgumentParser(description='Generate a brute force dictionary.')
parser.add_argument('--uppercase', '-C', dest='upper', action='store_true', default=False, help='Include upercase letters.')
parser.add_argument('--lowercase', '-c', dest='lower', action='store_true', default=True, help='Include lowercase letters.')
parser.add_argument('--digits', '-d', dest='digits', action='store_true', default=False, help='Include digits.')
parser.add_argument('--special', '-s', dest='special', action='store_true', default=False, help='Include special characters.')
parser.add_argument('--min', '-m', dest='min', type=int, default=3, help='Minimum characters in password.')
parser.add_argument('--max', '-M', dest='max', type=int, default=6, help='Maximum characters in password.')
parser.add_argument('--remove-dupes', '-r', metavar='N', dest='remove', type=int, default=None, help='Remove passwords that hae adjoined characters that are repeated N times.')
parser.add_argument('--file', '-f', dest='outfile', type=str, nargs='?', help='Filename to write to. If not specified, stdout.')
parser.add_argument('--append', dest='append', action='store_true', help='DO NOT recreate FILE, just append to it.')
parser.add_argument('--debug', dest='debug', action='store_true', help='Print debugging information.')
parser.add_argument('--marks', dest='marks', action='store_true', help='Print good/badd password marks.  WARNING: LOTS OF OUTPUT')
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

if args.debug:
    print('debug: pool: %s' % pool)

# setup the file to append to(if applicable) and delete the previous one
if not args.append:
    if os.path.exists(args.outfile):
        if args.debug:
            print('debug: deleting original file')
        os.remove(args.outfile)

if args.outfile:
    if args.debug:
        print('debug: opening file: %s' % args.outfile)
    file_handler = open(args.outfile, "a")
else:
    if args.debug:
        print('debug: using stdout for output')
    file_handler = None

# Print a handy summary of what's about to happen.
print("+====================================================================+")
print("| We're about to start generating brute force dictionary.  This will |")
print("| take quite a while.  Review the configuration below before starting|")
print("+--------------------------------------------------------------------+")
print("| Output file: {0: <54}|".format(args.outfile + (' (append)' if args.append else ' ' )))
print("| Uppercase: {0: <56}|".format('yes' if args.upper else 'no '))
print("| Lowercase: {0: <56}|".format('yes' if args.lower else 'no '))
print("| Numbers: {0: <58}|".format('yes' if args.digits else 'no '))
print("| Special Characters: {0: <47}|".format('yes' if args.special else 'no '))
print("| Minimum Length: {0: <51}|".format(args.min if args.min else ''))
print("| Maximum Length: {0: <51}|".format(args.max if args.max else ''))
print("| Remove Repeats Of Characters: {0: <38}|".format(args.remove if args.remove else 'no '))
print("| Append to file: {0: <51}|".format('yes' if args.upper else 'no '))
print("+====================================================================+")
try:
    input("Press <ENTER> to continue.")
except KeyboardInterrupt: 
    print('\n')
    file_handler.close()
    sys.exit(0)

def generate_by_length(length):
    """ Generate passwords that are X long """
    products = itertools.product(pool, repeat=length)
    for i in products: 
        write_it = True

        # removing passwords that have repeating characters if remove 
        # option is used.
        if args.remove > 1:
            p = r'\1' * (args.remove - 1)
            if re.match('(\w)' + p, ''.join(i)):
                if args.marks:
                    print(',', end="", flush=True)
                write_it = False
            else:
                if args.marks:
                    print('.', end="", flush=True)

        # write the password string
        if write_it:
            if file_handler:
                file_handler.write(''.join(i) + '\n')
                file_handler.flush()
            else:
                sys.stdout.write(''.join(i) + '\n')

# Generate the full range
x = args.min
try:
    while x <= args.max:
        if args.debug:
            print('debug: generating passowrds %s characters long' % x)
        generate_by_length(x)
        x += 1 
except KeyboardInterrupt:
    file_handler.close()
    sys.exit(0)

sys.exit(0)
