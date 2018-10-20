import numpy as np
import glob
import os
import math
import sys
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
file = open(current_directory+'/risultati', 'r')

correct=0

for line in file: 
    line_arr = line.split(",")
    print line_arr
    if line_arr[0]==line_arr[1]:
       correct+=1

print correct
      


    
