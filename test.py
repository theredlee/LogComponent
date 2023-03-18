# 1. asynchronous writing ✔
# 2. Midnight file update ✔
# 3. Stop by two ways: right away / wait for finishing the writing
# Error tolerance
# Unit test

from LogComponent import *
# ============================================================== Module Call Testing 2
LC = LogComponent()

with open(PATH + 'read_2mb.txt') as f:
    # lines = f.readlines()
    contents = f.read()
    LC.write(contents)
    # print(contents)

print("Enter interrupt keys: ")
x = input()
if x=='stop 1': # stop by the wait for it to finish writing outstanding logs if any
    LC.run_event.clear()
    LC.th2.join()
    LC.th1.join()
    print("Both threads successfully closed.")
    sys.exit(1)
elif x=='stop 2': # stop right away and if any outstanding logs they are not written
    LC.run_event.clear()
    print("Both threads stopped right away successfully.")
    sys.exit(1)