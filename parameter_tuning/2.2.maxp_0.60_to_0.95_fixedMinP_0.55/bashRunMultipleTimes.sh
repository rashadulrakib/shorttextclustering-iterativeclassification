#!/bin/bash
fixedMinP=0.50
fraction=0.05
#maxP=0.95
for j in `seq 1 9`;
do  
    t=$(echo $j*$fraction | bc)  
	maxP=`echo $t + $fixedMinP | bc` #fixed percentage for training data
	totalSec=0
    for i in `seq 1 20`; #experiments
    do
	    echo $i
        echo $maxP             
        START=$(date +"%T")
	    #echo "before time : $START"
	    python itr_clustering_multipass_external_arg_classification.py $i $fixedMinP $maxP> tweet-2472-kmeans-we-lr-tfidf-out$i-$fixedMinP-$maxP
		  
 	    #python itr_clustering_multipass_classification.py  > tweet2472-hc-nbyk-we-lr-tfidf-if-out$i
        END=$(date +"%T")
        #echo "after time : $END"
        SEC1=`date +%s -d ${START}`
	    SEC2=`date +%s -d ${END}`
        DIFFSEC=`expr ${SEC2} - ${SEC1}`
	    echo "It took $DIFFSEC seconds"
		totalSec=`echo $totalSec + $DIFFSEC | bc`  
    done
	echo "average run-time $((totalSec / 20)) seconds"
done  
