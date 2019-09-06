import glob
import numpy as np

filelist=glob.glob("/home/owner/PhD/clustering-iterative-classification-tfidf/parameter_tuning/2.1.minp_0.4_to_0.85_fixedMaxP_0.9/2.1.tweet-2472-kmeans-we-lr-tfidf/*")
print(len(filelist))

nmiDic={}
purityDic={}

for fileName in filelist:
 arr=fileName.split('-')
 #print(fileName) 
 fileKey=arr[len(arr)-2]+"-"+arr[len(arr)-1]
 #print(fileKey)
 
 file=open(fileName,"r")
 lines=file.readlines()
 file.close()
 
 tlines=len(lines)
 nmi=str(lines[tlines-3]).strip().replace("nmi_score-whole-data:   ",'')  
 purity=str(lines[tlines-1]).strip().replace("purity majority whole data=",'')
 #print(fileKey+"\t"+purity+"\t"+nmi)
 nmiDic.setdefault(fileKey, []).append(float(nmi))
 purityDic.setdefault(fileKey, []).append(float(purity))
 
#print(nmiDic) 
#print(purityDic)
for key in purityDic.keys(): 
 nmis= nmiDic[key] 
 nmis=np.array(nmis)
 nmi_mean=np.mean(nmis)
 nmi_std=np.std(nmis)
 
 purities=purityDic[key]
 purities=np.array(purities)
 purity_mean=np.mean(purities)
 purity_std=np.std(purities)
 
 print("minP-maxP="+key+",purity_mean="+str(purity_mean)+",purity_std="+str(purity_std)+",nmi_mean="+str(nmi_mean)+",nmi_std="+str(nmi_std))
