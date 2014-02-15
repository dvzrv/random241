#import OSC as osc
import liblo as osc
import logging

# Declare an empty target
target = None


# Connect to the server
def connect_to_server(hostname, port):
    global target
    if (hostname or port) is None:
        target = osc.Adress('127.0.0.1', 57121, osc.UDP)
    else:
        try:
            target = osc.Address(hostname, port, osc.UDP)
        except osc.AddressError, err:
            logging.error(err)


# Send a osc_message to the server
def send_msg(time_delta, randomness):
    global target
    # if the message is not empty and longer than 1
    if randomness is not None and len(randomness) > 1:
        msg = osc.Message("/random")
        msg.add(time_delta)
        msg.add(randomness[0], randomness[1])
        try:
            osc.send(target, msg)
        except:
            logging.error('OSC: Sending of message failed.')
