import numpy as np
arr = np.arange(5)
print("data :")
print(arr)
np.save('journalDev.npy', {"1":1})
print("Your array has been saved to journalDev.npy")

arr = np.load('journalDev.npy',allow_pickle=True)
print("The data is:")
print(arr)
