import random

minP=50
maxP=95

samples=1000000
diffSum=0
sumTrainRatio=0

for i in range(samples):
 currentPercent=random.uniform(minP, maxP)/100
 sumTrainRatio=sumTrainRatio+currentPercent
 if i>0:
   #print("prev %f, present %f" % (prevPercent, currentPercent ))
   diffSum=diffSum+abs(prevPercent-currentPercent)
 prevPercent=currentPercent
 

avg_diff_trainRatio= diffSum/(samples-1)
print("avg_diff_trainRatio= " , avg_diff_trainRatio)
print("sumTrainRatio= ", sumTrainRatio/float(samples))
