# # import shutil
# # import os

# # root = os.getcwd()
# # testdir = os.path.join(root, "testdir")
# # if not(os.path.isdir(testdir)):
# #     os.mkdir(testdir)
# #     print(testdir)
# #     print(dir(shutil.disk_usage(testdir)))
# # else:
# #     shutil.rmtree(testdir)

# mantap = {
#     "m" : 12234,
#     "n" : 21345
# }

# print(mantap)
# del mantap['m']
# print(mantap)

from datetime import datetime
from time import sleep

updated = datetime.now()
sleep(10)
print(updated.second != datetime.now().second)