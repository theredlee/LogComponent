# 1. asynchronous writing ✔
# 2. Midnight file update ✔
# 3. Stop by two ways: right away / wait for finishing the writing
# Error tolerance
# Unit test

from LogComponent import *

# ============================================================== Module Call Testing 1
# timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S.%f')[:-7]
# print(timestamp[:-9])

# with open(PATH + 'read_2mb.txt') as f:
#     # lines = f.readlines()
#     contents = f.read()
#     LC.write(contents)
#     # print(contents)

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     LC.run_event.clear()
#     LC.th1.join()
#     print("Thread successfully closed.")
#     sys.exit(1)


# ============================================================== Module Call Testing 2
LC = LogComponent()

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
    LC.th1.join()
    LC.th2.join()
    print("Both threads successfully closed.")
    sys.exit(1)