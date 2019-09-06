fileNamePrefix="googlenews-ts-kmeans---we-lr-tfidf-if-out"

for i in range(20):
 fileSuffix=i+1
 fileName=fileNamePrefix+str(fileSuffix)
 #print(fileName)
 file=open(fileName,"r")
 lines=file.readlines()
 tlines=len(lines)
 nmiLine=str(lines[tlines-2]).strip().replace("nmi_score-whole-data:   ",'')  
 purityLine=str(lines[tlines-1]).strip().replace("purity majority whole data=",'')
 print(purityLine+"\t"+nmiLine) 
 file.close()
 
