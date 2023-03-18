# 1. asynchronous writing ✔
# 2. Midnight file update ✔
# 3. Stop by two ways: right away / wait for finishing the writing
# Error tolerance
# Unit test

import os
import threading
import time
import aiofiles
import asyncio
from datetime import datetime
import sys

PATH = "./"
LOG_PATH = "./logs/"
WRITE_FILE = 'write_test.log'

class LogComponent:

    def __init__(self):
        self.conn = None
        self.loop = asyncio.get_event_loop()
        self.run_event = threading.Event()
        self.run_event.set()
        self.th = threading.Thread(target=self.check_log_folder, args=())
        self.th.start()
    
    def get_time(self): # to second
        return datetime.now().strftime('%Y%m%d_%H_%M_%S.%f')[:-7]
    
    def check_log_folder(self):
        
        while self.run_event.is_set():
            timestamp = self.get_time()
            date = timestamp[:-9]
            folder = LOG_PATH + date
            
            # Check daily folder
            if not os.path.exists(folder):
                try: 
                    os.mkdir(folder)
                    print("Log direcotry '" + folder + "' created successfully.")
                except OSError as error: 
                    print(error) 
            
            # Sleep for 1 second
            time.sleep(1)
    
    def get_file_name(self):

        timestamp = self.get_time()
        hour = timestamp[:-6]
        date = timestamp[:-9]
        folder = LOG_PATH + date
        
        # Hour-based writing
        while not os.path.exists(folder):
            try:
                raise Exception("Log direcotry '" + folder + "' does not exist.")
            except ValueError as e:
                print(e)
            # Sleep for 1 second
            time.sleep(1)

        file_name = folder + "/" + hour + "_" + WRITE_FILE
        print("Ready to write to '" + file_name + " .")
        
        # return file name
        return file_name

    def write(self, line):
        return self.loop.run_until_complete(self._async_write_(line))

    async def _async_write_(self, line):
        async with aiofiles.open(self.get_file_name(), mode='a') as f:
            await f.write(line)
            await f.flush()

# ==============================================================
# LC = LogComponent()
# LC.write()

# ==============================================================
# asyncio.run(LC.write())
# loop = asyncio.get_event_loop()
# server = loop.run_until_complete(write())

# ============================================================== Module Call Testing

LC = LogComponent()

timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S.%f')[:-7]
# print(timestamp[:-9])

with open(PATH + 'read_2mb.txt') as f:
    # lines = f.readlines()
    contents = f.read()
    LC.write(contents)
    # print(contents)

try:
    while True:
        pass
except KeyboardInterrupt:
    LC.run_event.clear()
    LC.th.join()
    print("Thread successfully closed.")
    sys.exit(1)