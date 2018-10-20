import numpy as np
import glob
import os
import math
import sys
import shutil

for iter_num in xrange(1,2):
 current_directory = os.path.dirname(os.path.abspath(__file__))
 file = open(current_directory+'/risultati', 'r')

 correct=0
 for line in file: 
    line_arr = line.split(",")
    if line_arr[0]==line_arr[1][:-1]:
       correct+=1

 print correct
    
