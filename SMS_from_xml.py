import os
from xml.etree import ElementTree

#converts to INCOMING or OUTGOING
def str_to_text(s):
    if s == 'true':
        return 'INCOMING'
    elif s == 'false':
        return 'OUTGOING'
    else:
        raise ValueError("Cannot covert {}".format(s))

#Converts string to boolean
def str_to_bool(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        raise ValueError("Cannot covert {} to a bool".format(s))



file_name = input("The name of the file with messages: ")
full_file = os.path.abspath(file_name)

dom = ElementTree.parse(full_file)
messages = dom.findall('Message')

output_file = input("Name of output file: ")
phone = input("Phone number to look for: ")
with open(output_file, 'w') as f:
    for m in messages:
        isIncoming = m.find('IsIncoming').text
        if str_to_bool(isIncoming):
            number = m.find('Sender').text
        else:
            number = m.find('Recepients').find('string')
            if not (number == None):
                number = number.text
        if not (number == None):
            if (phone in number):
                state = str_to_text(isIncoming)
                body = m.find('Body').text
                f.write("{}\t{}\n{}\n\n".format(number, state, body))
print("DONE!")
