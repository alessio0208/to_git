import numpy as np
import glob
import os
import math
import sys
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
path= current_directory + '/iter1'

results=np.zeros((7500, 4))

for f in os.listdir(path):

  if f.endswith(".distance"):
    file = open(path+'/'+f, 'r')
    i=0 
    for line in file: 
        if ',' in line:
           line_arr = line.split(",")
           current_dist = line_arr[2]

           if results[i][0]!=0:   
              #print results[i]   
              if float(current_dist) > float(results[i][2]):
                 results[i]=line_arr
           else:     
              results[i]=line_arr  
           
            
        i+=1
       
    file.close()


with open(current_directory+'/'+"risultati", 'w') as f:
    for item in results:
        j=0
        for i in item:
            if j==0 or j==1:            
               f.write("%s," % int(i))
             
              

        f.write("\n")


