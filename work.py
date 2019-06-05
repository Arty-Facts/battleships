import os

os.system(f"py traine_nn.py taghunt300k_lern100k taghunt300k_lern110k")
for i in range(1, 100):
    os.system(f"py traine_nn.py taghunt300k_lern1{i}0k taghunt300k_lern1{i+1}0k")

