import os
from send_handler import send_handler

with open(os.path.realpath('logtmp/2020_10_26_15_47_13_tmplog'), 'r') as f:
    send_handler(f)
