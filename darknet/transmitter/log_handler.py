import os
import glob
from datetime import datetime
from .send_handler import send_handler

class LogHandler:

    def __init__(self):
        self.start_time = datetime.now()
        self.wait_time = 10
        self.file = None
        self.folder = 'logtmp'
        self.create_file()

    def detection(self, results):
        current_time = datetime.now()
        time_delta = current_time - self.start_time
        if time_delta.total_seconds() > self.wait_time:
            self.start_time = current_time
            send_handler(self.file)
            self.remove_file()
            self.create_file()
        with open(os.path.realpath(self.file.name), 'a') as f:
            for line in results:
                f.write(str(line)+'\n')

    def create_file(self):
        timestamp = self.start_time.strftime("%Y_%m_%d_%H_%M_%S")
        f = open(os.path.dirname(os.path.abspath(__file__))+'/'+self.folder+'/'+timestamp+"_tmplog", "w+")
        f.close
        self.file = f

    def remove_file(self):
        os.remove(os.path.realpath(self.file.name))

# Class DataHandler:
# normalize all data rows for one input to DB

# Class SendHandler:
# send normalized data
