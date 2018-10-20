import numpy as np
import glob
import os
import math
import sys
import shutil


for iter_num in xrange(1,10): 
 current_directory = os.path.dirname(os.path.abspath(__file__))
 path= current_directory + '/iter'+str(iter_num)

 results=np.zeros((7500, 4))

 for f in os.listdir(path):

  if f.endswith(".distance"):
    file = open(path+'/'+f, 'r')
    i=0 
    for line in file: 
        if ',' in line:
           line_arr = line.split(",")

           if results[i][0]!=0:   
              #print results[i]   
              if line_arr[0] == line_arr[1]:
                 results[i]=line_arr
           else:     
              results[i]=line_arr  
           
            
        i+=1
       
    file.close()


 with open(current_directory+'/result'+str(iter_num), 'w') as f:
    for item in results:
        j=0
        for i in item:
            if j==0 or j==1:            
               f.write("%s," % int(i))
            # else :
             #  f.write("%s," % i)
            j+=1  

        f.write("\n")


