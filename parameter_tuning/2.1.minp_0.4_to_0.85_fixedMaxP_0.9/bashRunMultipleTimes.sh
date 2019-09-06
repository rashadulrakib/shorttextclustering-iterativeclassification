#!/bin/bash
fixedMaxP=0.9
fraction=0.05
initMinP=0.35
for j in `seq 1 10`;
do  
    t=$(echo $j*$fraction | bc)  
	minP=`echo $t + $initMinP | bc` #fixed percentage for training data
	totalSec=0
    for i in `seq 1 20`; #experiments
    do
	    echo $i
        echo $minP             
        START=$(date +"%T")
	    #echo "before time : $START"
	    #python itr_clustering_multipass_external_arg_classification.py $i $minP $fixedMaxP> websnippet-2280-kmeans-we-lr-tfidf-out$i-$minP-$fixedMaxP
		
		python itr_clustering_multipass_external_arg_classification.py $i $minP $fixedMaxP> tweet-2472-kmeans-we-lr-tfidf-out$i-$minP-$fixedMaxP
		  
        END=$(date +"%T")
        #echo "after time : $END"
        SEC1=`date +%s -d ${START}`
	    SEC2=`date +%s -d ${END}`
        DIFFSEC=`expr ${SEC2} - ${SEC1}`
	    echo "It took $DIFFSEC seconds"
		totalSec=`echo $totalSec + $DIFFSEC | bc`  
    done
	echo "average run-time $((totalSec / 1)) seconds"
done  
