from read_clust_label import readClustLabel
from combine_predtruetext import combinePredTrueText
from groupTxt_ByClass import groupTxtByClass
from word_vec_extractor import populateTermVecs
from nltk.tokenize import word_tokenize
from sent_vecgenerator import generate_sent_vecs_toktextdata
from generate_TrainTestTxtsTfIdf import comPrehensive_GenerateTrainTestTxtsByOutliersTfIDf
from generate_TrainTestVectorsTfIdf import generateTrainTestVectorsTfIDf
from sklearn.linear_model import LogisticRegression
from time import time
from sklearn import metrics
from nltk.corpus import stopwords
from txt_process_util import processTxtRemoveStopWordTokenized
import re
import numpy as np
import random
import sys
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from outlier_detection_sd import detect_outlier_sd_vec
from compute_util import MultiplyTwoSetsOneToOne

minIntVal = -1000000
numberOfClusters =89
maxIterations=50
#maxTrainRatio =0.85
#minTrainRatio = 0.60
#fixedMinPercent = 70
#maxPercent = 85
#percentIncr = 5
extParam = str(sys.argv[1])
print(extParam)
fixedMinP = float(str(sys.argv[2]))*100
print(fixedMinP)
maxP = float(str(sys.argv[3]))*100
print(maxP)
maxTrainRatio =maxP

#trainFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/train"
#testFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/test"
#traintestFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/traintest"
#textsperlabelDir="/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/semisupervised/textsperlabel/"
#dataFileTxtTrue = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/googlesnippetraw-2280"
#extClustFile = "/home/owner/PhD/clustering-k-means/websnippet-2280-we-kmeans-run"+extParam

trainFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/tweet/2472/train"
testFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/tweet/2472/test"
traintestFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/tweet/2472/traintest"
textsperlabelDir="/home/owner/PhD/dr.norbert/dataset/shorttext/tweet/2472/semisupervised/textsperlabel/"
dataFileTxtTrue = "/home/owner/PhD/dr.norbert/dataset/shorttext/tweet/2472/tweet-original-order.txt"
extClustFile = "/home/owner/PhD/clustering-k-means/tweet-we-kmeans-run"+extParam

last_homoginity=0
last_purity_custom=0
last_nmi=0
last_completeness=0

def WriteTrainTest(listtuple_pred_true_text, outFileName):
 file2=open(outFileName,"w")
 for i in range(len(listtuple_pred_true_text)):
  file2.write(listtuple_pred_true_text[i][0]+"\t"+listtuple_pred_true_text[i][1]+"\t"+listtuple_pred_true_text[i][2]+"\n")

 file2.close()


def ReadPredTrueText(InFileName):
 file1=open(InFileName,"r")
 lines = file1.readlines()
 file1.close()
 listtuple_pred_true_text = []
 for line in lines:
  line = line.strip()
  arr = re.split("\t", line)
  predLabel = arr[0]
  trueLabel = arr[1]
  text = arr[2]
  tupPredTrueTxt = [predLabel, trueLabel, text]
  listtuple_pred_true_text.append(tupPredTrueTxt) 
 
 return listtuple_pred_true_text


def MergeAndWriteTrainTest():
 print(extClustFile)
 clustlabels=readClustLabel(extClustFile)
 listtuple_pred_true_text, uniqueTerms=combinePredTrueText(clustlabels, dataFileTxtTrue)
 WriteTrainTestInstances(traintestFile, listtuple_pred_true_text)
 return listtuple_pred_true_text 


def WriteTextsOfEachGroup(labelDir, dic_tupple_class):
 for label, value in dic_tupple_class.items():
  labelFile = labelDir+label
  file1=open(labelFile,"w")
  for pred_true_txt in value:
   file1.write(pred_true_txt[0]+"\t"+pred_true_txt[1]+"\t"+pred_true_txt[2]+"\n")

  file1.close()

def Gen_WriteOutliersEachGroup(labelDir, numberOfClusters):
 dic_label_outliers = {}
 for labelID in range(numberOfClusters):
  fileId = labelID +1 
  labelFile = labelDir+str(fileId)
  file1=open(labelFile,"r")
  lines = file1.readlines()
  file1.close()
  
  train_data = []
  train_labels = []
  train_trueLabels = []

  for line in lines:
   line=line.lower().strip() 
   arr = re.split("\t", line)
   train_data.append(arr[2])
   train_labels.append(arr[0])
   train_trueLabels.append(arr[1])

  vectorizer = TfidfVectorizer( max_df=1.0, min_df=1, stop_words='english', use_idf=True, smooth_idf=True, norm='l2')
  x_train = vectorizer.fit_transform(train_data)

  contratio = 0.1
  #isf = IsolationForest(n_estimators=100, max_samples='auto', contamination=contratio, max_features=1.0, bootstrap=True, verbose=0, random_state=0, behaviour='new')
  isf=IsolationForest(n_estimators=100, max_samples='auto', contamination=contratio, max_features=1.0, bootstrap=True, verbose=0, random_state=0)
  outlierPreds = isf.fit(x_train).predict(x_train)
  dic_label_outliers[str(fileId)] = outlierPreds  #real
  
  #dense_x_train = x_train.toarray()
  #outlierPreds_sd = detect_outlier_sd_vec(dense_x_train, 0.1)
  #outlierPredsMult = MultiplyTwoSetsOneToOne(outlierPreds, outlierPreds_sd)
  #outlierPreds=outlierPreds_sd
  #dic_label_outliers[str(fileId)] = outlierPreds #outlierPreds_sd #outlierPredsMult

  file1=open(labelDir+str(fileId)+"_outlierpred","w")
  for pred in outlierPreds:
   file1.write(str(pred)+"\n") 
 
  file1.close()
 
 return dic_label_outliers
 


def WriteTrainTestInstances(instFile, tup_pred_true_txts):
 file1=open(instFile,"w")
 for tup_pred_true_txt in tup_pred_true_txts:
  file1.write(tup_pred_true_txt[0]+"\t"+tup_pred_true_txt[1]+"\t"+tup_pred_true_txt[2]+"\n")  

 file1.close()



def GenerateTrainTest2_Percentage(percentTrainData):
 trainDataRatio = 1.0
		
 listtuple_pred_true_text = ReadPredTrueText(traintestFile)
 perct_tdata = percentTrainData/100
 goodAmount_txts = int(perct_tdata*(len(listtuple_pred_true_text)/numberOfClusters))			
 dic_tupple_class=groupTxtByClass(listtuple_pred_true_text, False)		
 #write texts of each group in  
 WriteTextsOfEachGroup(textsperlabelDir,dic_tupple_class)
 dic_label_outliers = Gen_WriteOutliersEachGroup(textsperlabelDir, numberOfClusters)

 train_pred_true_txts = []
 test_pred_true_txts = []

 for label, pred_true_txt in dic_tupple_class.items():
  outlierpreds = dic_label_outliers[str(label)]
  pred_true_txts = dic_tupple_class[str(label)]

  if len(outlierpreds)!= len(pred_true_txts):
   print("Size not match for="+str(label))
  
  outLiers_pred_true_txt = []
  count = -1
  for outPred in outlierpreds:
   outPred = str(outPred)
   count=count+1
   if outPred=="-1":
    outLiers_pred_true_txt.append(pred_true_txts[count])

  test_pred_true_txts.extend(outLiers_pred_true_txt)
  #remove outlierts insts from pred_true_txts
  pred_true_txts_good = [e for e in pred_true_txts if e not in outLiers_pred_true_txt]
  dic_tupple_class[str(label)]=pred_true_txts_good

  
 for label, pred_true_txt in dic_tupple_class.items():
  pred_true_txts = dic_tupple_class[str(label)] 
  pred_true_txt_subs= []
  numTrainGoodTexts=int(perct_tdata*len(pred_true_txts))
  if len(pred_true_txts) > goodAmount_txts:
   pred_true_txt_subs.extend(pred_true_txts[0:goodAmount_txts])
   test_pred_true_txts.extend(pred_true_txts[goodAmount_txts:len(pred_true_txts)]) 
  else:
   pred_true_txt_subs.extend(pred_true_txts)
  train_pred_true_txts.extend(pred_true_txt_subs)
 
 trainDataRatio = len(train_pred_true_txts)/len(train_pred_true_txts+test_pred_true_txts)
 print("trainDataRatio="+str(trainDataRatio))
 #if trainDataRatio<=maxTrainRatio:
 WriteTrainTestInstances(trainFile,train_pred_true_txts)
 WriteTrainTestInstances(testFile,test_pred_true_txts) 
   		
 return trainDataRatio
 


def PerformClassification(trainFile, testFile, traintestFile):
 file=open(trainFile,"r")
 lines = file.readlines()
 #np.random.seed(0)
 np.random.shuffle(lines)
 file.close()

 train_data = []
 train_labels = []
 train_trueLabels = []

 for line in lines:
  line=line.strip().lower() 
  arr = re.split("\t", line)
  train_data.append(arr[2])
  train_labels.append(arr[0]) #train_labels.append(arr[0])
  train_trueLabels.append(arr[1])
 
 file=open(testFile,"r")
 lines = file.readlines()
 file.close()

 test_data = []
 test_labels = []

 for line in lines:
  line=line.strip().lower() 
  arr = re.split("\t", line)
  test_data.append(arr[2])
  test_labels.append(arr[1])

 vectorizer = TfidfVectorizer( max_df=1.0, min_df=1, stop_words='english', use_idf=True, smooth_idf=True, norm='l2')
 X_train = vectorizer.fit_transform(train_data)
 X_test = vectorizer.transform(test_data)
 
 #clf = LogisticRegression(solver='lbfgs', multi_class='auto') #52
 clf = LogisticRegression() #52
 #t0 = time()
 clf.fit(X_train, train_labels)
 #train_time = time() - t0
 #print ("train time: %0.3fs" % train_time)

 #t0 = time()
 pred = clf.predict(X_test)
 #test_time = time() - t0
 #print ("test time:  %0.3fs" % test_time)

 y_test = [int(i) for i in test_labels]
 pred_test = [int(i) for i in pred]
 #score = metrics.homogeneity_score(y_test, pred_test)
 #print ("homogeneity_score-test-data:   %0.4f" % score)
 #score = metrics.normalized_mutual_info_score(y_test, pred_test)  
 #print ("nmi_score-test-data:   %0.4f" % score) 
 
 file=open(traintestFile,"w")
 for i in range(len(train_labels)):
  file.write(train_labels[i]+"\t"+train_trueLabels[i]+"\t"+train_data[i]+"\n")

 for i in range(len(test_labels)):
  file.write(pred[i]+"\t"+test_labels[i]+"\t"+test_data[i]+"\n")
 
 file.close()


def ComputePurity(dic_tupple_class):
 totalItems=0
 maxGroupSizeSum =0
 for label, pred_true_txts in dic_tupple_class.items():
  totalItems=totalItems+len(pred_true_txts)
  dic_tupple_class_originalLabel=groupTxtByClass(pred_true_txts, True)
  maxMemInGroupSize=minIntVal
  maxMemOriginalLabel=""
  for orgLabel, org_pred_true_txts in dic_tupple_class_originalLabel.items():
   if maxMemInGroupSize < len(org_pred_true_txts):
    maxMemInGroupSize=len(org_pred_true_txts)
    maxMemOriginalLabel=orgLabel
  
  maxGroupSizeSum=maxGroupSizeSum+maxMemInGroupSize
  
 purity=maxGroupSizeSum/totalItems
 print("purity majority whole data="+str(purity))
 last_purity_custom=purity
 return purity

 
def EvaluateByPurity(traintestFile):
 listtuple_pred_true_text = ReadPredTrueText(traintestFile)
 preds = []
 trues = []
 for pred_true_text in listtuple_pred_true_text:
  preds.append(pred_true_text[0])
  trues.append(pred_true_text[1])
 
 score = metrics.homogeneity_score(trues, preds)
 last_homoginity=score
 print ("homogeneity_score-whole-data:   %0.4f" % score)   			
 #score = metrics.normalized_mutual_info_score(trues, preds, average_method='arithmetic')
 score = metrics.normalized_mutual_info_score(trues, preds) 
 last_nmi=score
 print ("nmi_score-whole-data:   %0.4f" % score)
 last_completeness=metrics.completeness_score(trues, preds)
 print("completeness="+str(last_completeness))
 dic_tupple_class=groupTxtByClass(listtuple_pred_true_text, False)
 return ComputePurity(dic_tupple_class)


def GenerateTrainTest2List(listtuple_pred_true_text, fixedMinP, maxP):
 print("Initial---------")
 EvaluateByPurity(traintestFile)

 for itr in range(maxIterations):
  randPercent=random.uniform(fixedMinP, maxP)
  trainDataRatio = GenerateTrainTest2_Percentage(randPercent);
  print(str(itr)+","+str(randPercent))
  PerformClassification(trainFile, testFile, traintestFile)
  EvaluateByPurity(traintestFile)

  
listtuple_pred_true_text = MergeAndWriteTrainTest()
GenerateTrainTest2List(listtuple_pred_true_text, fixedMinP, maxP)

#print("last_homoginity="+str(last_homoginity))
#print("last_purity_custom="+str(last_purity_custom))
#print("last_completeness="+str(last_completeness))
#print("last_nmi="+str(last_nmi))

