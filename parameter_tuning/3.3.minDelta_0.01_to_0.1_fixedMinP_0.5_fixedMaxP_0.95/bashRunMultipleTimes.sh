#!/bin/bash
fixedMinP=0.5
fixedMaxP=0.95
fraction=0.01 #0.01 to 0.04

for j in `seq 1 10`;
do  
    minDelta=$(echo $j*$fraction | bc)  
	totalSec=0
    for i in `seq 1 20`; #experiments
    do
	    echo $i
        echo $minDelta             
        START=$(date +"%T")
	    #echo "before time : $START"
	    python itr_clustering_multipass_external_arg_classification.py $i $fixedMinP $fixedMaxP $minDelta> websnippet-2280-kmeans-we-lr-tfidf-out$i-$fixedMinP-$fixedMaxP-$minDelta
		  
 	    #python itr_clustering_multipass_classification.py  > tweet2472-hc-nbyk-we-lr-tfidf-if-out$i
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
