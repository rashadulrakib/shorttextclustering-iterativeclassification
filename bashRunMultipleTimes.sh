#!/bin/bash
for i in `seq 1 1`;
do
	echo $i
        START=$(date +"%T")
	echo "before time : $START"
	#python itr_clustering_multipass_external_arg_classification.py $i > googlenews-s-kmeans---we-lr-tfidf-if-out$i
 	python itr_clustering_multipass_classification.py $i > bash_out_python_version_check
        END=$(date +"%T")
	echo "after time : $END"
        SEC1=`date +%s -d ${START}`
	SEC2=`date +%s -d ${END}`
        DIFFSEC=`expr ${SEC2} - ${SEC1}`
	echo "It took $DIFFSEC seconds"
done
