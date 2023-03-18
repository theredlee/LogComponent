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
        # For check_log_folder: th1
        self.th1 = threading.Thread(target=self.check_log_folder, args=())
        self.th1.start()
        # For write: th2
        self.th2 = None

    def get_time(self): # to second
        return datetime.now().strftime('%Y%m%d_%H_%M_%S.%f')[:-7]
    
    def check_log_folder(self):
        print("Started check_log_folder thread successfully.")

        while self.run_event.is_set(): # for i in range(5):
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

            # print("check_log_folder at " + str(i) + " s ...")

        print('check_log_folder() closing down')
    
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
        # For write
        self.th2 = threading.Thread(target=self.loop.run_until_complete(self._async_write_(line)), args=())
        self.th2.start()

    async def _async_write_(self, line):
        print("Started _async_write_ thread successfully.")
        
        if self.run_event.is_set():
            try:
                async with aiofiles.open(self.get_file_name(), mode='a') as f:
                    await f.write(line)
                    await f.flush()
            except EnvironmentError as e:
                print(e)
        else:
            print('_async_write_() closing down')