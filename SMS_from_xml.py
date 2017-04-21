"""
Extract SMS from .xml file.

If number is specified, it will be filtered by it.
Created for Microsoft Lumia .msg file.
"""

import os
from xml.etree import ElementTree
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=str, default='',
                        help='Name of the input file')
    parser.add_argument('--o', type=str, default='',
                        help='Name of the output file')
    parser.add_argument('--n', type=str, default='',
                        help='Number to filter by. [OPTIONAL]')
    args = parser.parse_args()
    if not args.n:
        print("Phone \'{}\'".format(args.n))
    # If phone variable is empty and input or output argument is empty
    phone = input("Phone number to look for: ")\
        if not args.n and (not args.i or not args.o) else args.n
    input_file = input("The name of the file with messages: ")\
        if not args.i else args.i
    output_file = input("Name of output file: ")\
        if not args.o else args.o
    extract_message(input_file, output_file, phone)


def str_to_text(s):
    """Convert string boolean to INCOMING or OUTGOING."""
    if s == 'true':
        return 'INCOMING'
    elif s == 'false':
        return 'OUTGOING'
    else:
        raise ValueError("Cannot covert {}".format(s))


def str_to_bool(s):
    """Convert string to boolean."""
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        raise ValueError("Cannot covert {} to a bool".format(s))


def extract_message(input_file, output_file, phone):
    """Extract message from XML file."""
    full_file = os.path.abspath(input_file)
    try:
        dom = ElementTree.parse(full_file)
    except FileNotFoundError:
        print("Unable to find file.")
        exit()
    else:
        messages = dom.findall('Message')
        with open(output_file, 'w') as f:
            for m in messages:
                isIncoming = m.find('IsIncoming').tex
                if str_to_bool(isIncoming):
                    number = m.find('Sender').text
                else:
                    number = m.find('Recepients').find('string')
                    if number is not None:
                        number = number.text
                if number is not None:
                    if (phone in number):
                        state = str_to_text(isIncoming)
                        body = m.find('Body').text
                        f.write("{}\t{}\n{}\n\n".format(number, state, body))
        print("DONE!")


if __name__ == "__main__":
    main()
