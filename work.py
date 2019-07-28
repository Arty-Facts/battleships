import os

os.system(f"py traine_nn.py init 10H100k")
for i in range(1, 100):
    os.system(f"py traine_nn.py 10H{i}00k 10H{i+1}00k")

