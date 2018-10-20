#!/usr/bin/python

import numpy as np
import glob
import os
import math
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from numpy import loadtxt
from scipy.spatial import distance
import sys
import shutil


arraySites = np.array([])
siti = []


directory=sys.argv[1]
directory=directory[:-1]

current_directory = os.path.dirname(os.path.abspath(__file__))

#print "CURRENT DIRECTORY ", current_directory
path = current_directory +'/'+ directory

j=True

numPoints=0
for filename in os.listdir(path):
   numPoints+=1
   file_path = os.path.join(path, filename)
   Z = loadtxt(fname=file_path, comments="#", delimiter="\n", unpack=False)   

   if j :
     arraySites = np.array([Z])
     j = False
   else :
    arraySites = np.vstack([arraySites,Z])

   siti.append(filename) 




dicto={}
i=0
for j in arraySites:  
    dicto[str(j)] = siti[i]
    i=i+1



scaler = StandardScaler()


def clustering( X, s, phase) :
  
 global best_epsilon
 global best_num_clusters 
 global best_minPoints 
 global best_outliers_deviation
 global best_clusters
 global best_standard_deviation
 global best_outliers 
 global best_silhouette
  
 best_silhouette=-1
 best_epsilon= 0
 best_num_clusters = 0
 best_minPoints = 0
 best_outliers_deviation=1000
 best_clusters = [[]]
 best_standard_deviation = 0
 best_outliers = 0

 
 
 step_size=0.1
 iterations=50
 initialEps=0.3
 threshold=0
   

 current_it=1 
 while current_it <=  iterations:
 
   minPoints=10

   
   while minPoints < 25:
   
    current_clusters = [[]]
    variance_clusters= 0
    current_eps= initialEps +  step_size * current_it


    X = s.fit_transform(X)
    db = DBSCAN(eps=current_eps, min_samples = minPoints).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

  
    unique_labels = set(labels)
  
   # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

#    print 'Current epsilon: ', current_eps, '; Current minPoints: ', minPoints
#    print 'Estimated number of clusters: ', n_clusters_
    
    current_outliers = len(X)
    X = s.inverse_transform(X)
   


    for k in zip(unique_labels):
  
      class_member_mask = (labels == k)
   
      if k == (-1,):
        xy = X[class_member_mask]
        current_outliers = len(xy)
      else:
        xy = X[class_member_mask]

    
      current_clusters.append(xy)


    current_clusters.pop(0)

    current_clusters_without_outliers= current_clusters[:-1]
   
    cluster_number=0
    cluster_lengths= []  
   
    biggest_cluster = 0
    for cl in current_clusters_without_outliers:
         
        cluster_lengths.append(len(cl))
        if len(cl) > biggest_cluster:
           biggest_cluster=len(cl)
      
 #       print "length cluster",cluster_number, " : ", cluster_lengths[cluster_number]
        cluster_number+=1
   
    variance_clusters = np.var(cluster_lengths)
    standard_deviation_clusters=math.sqrt(variance_clusters)
    if cluster_number>threshold and current_outliers<len(X): 
      current_silhouette=metrics.silhouette_score(X, labels)
          
      if current_silhouette > best_silhouette:
       

       best_epsilon  = current_eps
       best_num_clusters = n_clusters_
       best_minPoints = minPoints
       best_clusters = current_clusters
       best_standard_deviation = standard_deviation_clusters
       best_outliers = current_outliers
       best_silhouette = current_silhouette

    minPoints+=1
 
   current_it+=1



def printPartialResults(phase, directory_name):
 
 
 f1=open(current_directory+ '/result_'+str(directory_name), 'w')
# print "\n+++ RESULTS +++ "
 global resultPhase1
 resultPhase1=[[]]


# print "best epsilon ", best_epsilon
 f1.write("\nbest epsilon "+ str(best_epsilon))

# print "best number of clusters ", best_num_clusters
 f1.write("\nbest number of clusters "+ str(best_num_clusters))

# print "best minPoints ", best_minPoints
 f1.write("\nbest minPoints "+ str(best_minPoints))

# print "best outliers ", best_outliers
 f1.write("\nbest outliers " + str(best_outliers))

# print "best standard deviation ", best_standard_deviation, "\n"
 f1.write("\nbest standard deviation "+ str(best_standard_deviation))
  
# print "best silhouette ", best_silhouette
 f1.write("\nbest silhouette "+ str(best_silhouette))

 cluster=1

 for xy in best_clusters:

  
    if cluster < len(best_clusters) :
 #      print "CLUSTER ", cluster, "\n"
       f1.write("\n\nCLUSTER "+ str(cluster))
    else :
  #     print "OUTLIERS \n"
       f1.write("\n\nOUTLIERS ")
 
    
    clusterToFile= [] 

    for c in xy:
         try:
            clusterToFile.append(dicto[str(c)])
         except KeyError:
            print "ERROR WITH ", str(c)
            
    clusterToFile.sort()

    for site in clusterToFile : 
    #  print site
      f1.write("\n" +site)
    
  
    resultPhase1.append(clusterToFile)
    

   # print " "
    f1.write(" ")
    cluster+=1

 f1.close()



def printFinalResults(directory_name):
 
 fileStatistics= open(current_directory+ '/statistics_'+str(directory), 'w')
 fileFinalResults=open(current_directory+ '/finalResult_'+str(directory), 'w')
 

 global resultPhase2
 resultPhase2=[[]]

 cluster=1

 
 for xy in best_clusters_without_outliers:
      

    if cluster <= len(best_clusters_without_outliers) :
   
     clusterToFile= [] 
     for c in xy:
         try:
            clusterToFile.append(dicto[str(c)])
         except KeyError:
            print "ERROR WITH ", str(c)
            
    clusterToFile.sort()
    resultPhase2.append( clusterToFile)
    cluster+=1
 

 all_clusters_without_outliers=[[]]
 
 i=0
 while i < len(resultPhase2):
    all_clusters_without_outliers.append([])
    i+=1    


 for page in pagesList :
 
   maxOccurences=0
   cluster_maxOccurences = 0
   j=0 
  # print "PAGE ", page 
  
   for res in resultPhase2 :
     pageCount=0
     for r in res :
        if is_istance_of_page(page,r):
           pageCount+=1
           

     if pageCount > maxOccurences:
       maxOccurences = pageCount
       cluster_maxOccurences = j
  
     j+=1

  # print "MAX OCCURENCE ", maxOccurences, " IN CLUSTER ", cluster_maxOccurences,  "LEN ", len(all_clusters_without_outliers)
  
  
   for r in resultPhase2[cluster_maxOccurences]: 
       if is_istance_of_page(page, r):
          all_clusters_without_outliers[cluster_maxOccurences].append(r)
  

 
 finalResult=[[]]

 for res in all_clusters_without_outliers:
    if len(res) > 0 :
       finalResult.append(res)

 finalResult.pop(0)
 
   
 cluster=1
 for xy in finalResult:
    fileCluster= open(current_directory+ '/FR_cluster' + str( cluster) + '_'+ str(directory), 'w')  
   
    if cluster <= len(finalResult) :
   #    print "CLUSTER ", cluster, "\n"
       fileFinalResults.write("\n\nCLUSTER "+ str(cluster))
       fileStatistics.write("\nCLUSTER "+ str( cluster) + ": " + str(len(xy)))


    for site in xy : 
    #  print site
      fileFinalResults.write("\n" +site)
      fileCluster.write(site + "\n")
 
#    print " "
    fileFinalResults.write(" ")
    cluster+=1
    fileCluster.close()



 fileFinalResults.close()
 fileStatistics.close()



def is_istance_of_page(str1, str2):

 b = False
 i=0

 while i <15:
   pageAux= str1+'_'+str(i)
   pageAux2 = str1+'_'+str(i) + ' '
   if pageAux==str2 or pageAux2==str2:
      b=True 

   i+=1

 return b

def calculate_centroids_and_move_outliers():
   global best_clusters_without_outliers
   best_clusters_without_outliers=best_clusters[:-1]
   outliers = best_clusters[len(best_clusters)-1]

   i=0


   centroids=[]
   for x in best_clusters_without_outliers:
     centroids.append(np.average(x, axis=0))
 #    print centroids[i]
     i+=1

   for out in outliers:

     lowest_distance=1000000000000
     j=0
     best_j=0
     while j< len(centroids):
        
        dst = distance.euclidean(out, centroids[j])

        if dst < lowest_distance:

           lowest_distance=dst
           best_j=j
        
        j+=1
  #   print "BEST J",best_j
  #   print "OUT", out
     best_clusters_without_outliers[best_j]= np.append( best_clusters_without_outliers[best_j], [out], axis=0)


# #############################################################################
# Compute DBSCAN

clustering(X = arraySites, s= scaler, phase=1)
printPartialResults(phase=1, directory_name=directory)

calculate_centroids_and_move_outliers()

outliers = best_clusters[len(best_clusters)-1]

strFile=directory.replace('clustering','')

global pagesList
pagesList = [line.rstrip('\n') for line in open('listPages'+strFile)]


printFinalResults(directory_name=directory)




if "four" in str(directory):  
  siteName= directory[16:]

  if not os.path.exists(current_directory+ '/Final_results/' + siteName):
     os.makedirs(current_directory+ '/Final_results/' + siteName)
  if not os.path.exists(current_directory+ '/Final_results/' + siteName + '/all_instances_four_features'):
     os.makedirs(current_directory+ '/Final_results/' + siteName + '/all_instances_four_features')
  if not os.path.exists(current_directory+ '/Final_results/' + siteName + '/all_instances_four_features/clusters_files'):
     os.makedirs(current_directory+ '/Final_results/' + siteName + '/all_instances_four_features/clusters_files')
  
  all_instances=current_directory+ '/Final_results/'+ siteName + '/all_instances_four_features/' 


else:
  siteName= directory[11:]

  if not os.path.exists(current_directory+ '/Final_results/' + siteName):
     os.makedirs(current_directory+ '/Final_results/' + siteName)
  if not os.path.exists(current_directory+ '/Final_results/' + siteName + '/all_instances'):
     os.makedirs(current_directory+ '/Final_results/' + siteName + '/all_instances')
  if not os.path.exists(current_directory+ '/Final_results/' + siteName + '/all_instances/clusters_files'):
     os.makedirs(current_directory+ '/Final_results/' + siteName + '/all_instances/clusters_files')
    
  all_instances=current_directory+ '/Final_results/'+ siteName + '/all_instances/'


shutil.move(current_directory+ '/finalResult_'+str(directory), all_instances)    
shutil.move(current_directory+ '/listPages'+ str(strFile), all_instances) 
shutil.move(current_directory+ '/result_'+str(directory), all_instances)   
shutil.move(current_directory+ '/'+str(directory) , all_instances)  
shutil.move(current_directory+ '/statistics_'+str(directory), all_instances)  



for cluster in range (1, best_num_clusters+1):
    shutil.move(current_directory+ '/FR_cluster' + str( cluster) + '_'+ str(directory), all_instances + 'clusters_files/' )  












