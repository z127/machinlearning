# coding: utf-8
import csv
interval =['20','60','240'];
InLastPriceThreshold=['0.001'];
mycomputelatency=['6','10','20'];
outmubound = ['0.0001','0.0004'];
mubound = ['0.0001','0.0004'];

with open("h://parameter.csv", 'w') as csvfile:
    for i in range(len(interval)):
       for j in range(len(InLastPriceThreshold)):
           for k in range(len(mycomputelatency)):
               for l in range(len(mubound)):
                   for m in range(len(outmubound)):
                            spamwriter=csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                            #spamwriter.writerow(['a','b','v']);
                            #spamwriter.writerow(['a', '1', '1', '2', '2'])
                            #print()
                            spamwriter.writerow([mycomputelatency[k],interval[i],InLastPriceThreshold[j] , mubound[l] , outmubound[m]])


csvfile.close()