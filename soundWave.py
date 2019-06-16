import time
from random import randint, random
import math

total = 1000 #total samples
arr = []
freq = 1
increment = 1/freq

for i in range(total):
    arr.append(math.sin((math.pi / 2) * i / freq))

for f in range(100):
    print(arr[f])
#nice sine wave
