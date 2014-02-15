#!/usr/bin/python2

from sys import argv


def read_params():
    # Checks the given parameters
    info = """Use the program as following:
    random241.py [option] <param> ...
    Options:
        -c  number of cam to use (starts with first found camera 0 (default))
        -r  remote address to send the output to (standard 192.168.0.7)
    """
    default = {'-c': "1", '-r': "192.168.0.7"}
    parameters = default.copy()
    if len(argv) != 3:
        for i in xrange(1, len(argv) - 1, 2):
            if argv[i] in parameters:
                parameters[argv[i]] = argv[i + 1]
            else:
                print info
                return 0
        return parameters
    else:
        return default
