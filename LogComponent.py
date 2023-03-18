# 1. asynchronous writing ✔
# 2. Midnight file update
# 3. Stop by two ways: right away / wait for finishing the writing
# Error tolerance
# Unit test

import os
import aiofiles
import asyncio
from datetime import datetime

PATH = "./"
LOG_PATH = "./logs/"
WRITE_FILE = 'write_test.log'

class LogComponent:

    def __init__(self):
        self.conn = None
        self.loop = asyncio.get_event_loop()

    def get_time(self): # to second
        return datetime.now().strftime('%Y%m%d_%H_%M_%S.%f')[:-7]
    
    def get_file_name(self):
        timestamp = self.get_time()
        date = timestamp[:-9]
        folder = LOG_PATH + date

        if os.path.exists(folder):
            file_name = folder + "/" + self.get_time() + "_" + WRITE_FILE
        else:
            try: 
                os.mkdir(folder)
                file_name = folder + "/" + self.get_time() + "_" + WRITE_FILE
            except OSError as error: 
                print(error)  

        return file_name

    def write(self, line):
        return self.loop.run_until_complete(self._async_write_(line))

    async def _async_write_(self, line):
        async with aiofiles.open(self.get_file_name(), mode='a') as f:
            # await f.write(line + '\n')
            await f.write(line)
            await f.flush()

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