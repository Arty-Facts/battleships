import os

os.system(f"python traine_nn.py init 100k")
for i in range(1, 1000):
    os.system(f"python traine_nn.py {i}00k {i+1}00k")

