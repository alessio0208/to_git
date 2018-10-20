
import numpy as np
import glob
import os
import math
import sys
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
path= current_directory + '/iter5'

results=np.zeros((7500, 4))


for f in os.listdir(path):
  
  if f.endswith(".scaled"):
    print f
    file = open(path+'/'+f, 'r')
    i=0 
    for line in file: 
        if ',' in line:
           line_arr = line.split(",")
           line_arr = line_arr[:-1]
           print line_arr
           current_dist = line_arr[3]
           
           current_dist=current_dist[:-1]
           if results[i][0]!=0:   
              print current_dist, " +++ ", results[i][3]

              if float(current_dist) < float(results[i][3]):
                 print "ok"
                 results[i]=line_arr
           else:  
              print results[i], " ", line_arr   
              results[i]=line_arr  
           
           
        i+=1
       
    file.close()


with open(current_directory+'/'+"risultati", 'w') as f:
     for item in results:
        j=0
        for i in item:
            if j==0 or j==1:            
               f.write("%s," % int(i))
            else:
               f.write(str(i)+',')
            j+=1                 
              

        f.write("\n")


