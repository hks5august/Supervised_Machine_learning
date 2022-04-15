#!/bin/bash

cut -d, -f2- train_rna_pred_d1 >ss
perl -i -pe   's/^1,/+1,/g' ss 
perl -i -pe  's/^0,/-1,/g' ss
cut -d, -f1 ss |tail -n+2 >a

for i in `seq 2 13`;
        do
         	echo $i|cut -d, -f$i ss |tail -n+2>$i.b
         	name=`echo $i|cut -d, -f$i ss |head -1`
         	echo "\n" >>results_d
         	echo $name >>results_d
	 	paste -d" " a $i.b >data
	 	roc=`~/softwarekd/perf -roc < data | perl -pi -e 's/ROC//g' | perl -pi -e 's/ //g'`
	 	echo  "\tROC value\t$roc\n" >>results_d
	 	perl accuracy1_new.pl a $i.b results_d
	 	perl accuracy_new.pl a $i.b results_d
		rm $i.b data
	done   
cut -d, -f2- test_rna_pred_d1 >ss
perl -i -pe   's/^1,/+1,/g' ss
perl -i -pe  's/^0,/-1,/g' ss
cut -d, -f1 ss |tail -n+2 >a
for i in `seq 2 13`;
        do
                echo $i|cut -d, -f$i ss |tail -n+2>$i.b
         	name=`echo $i|cut -d, -f$i ss |head -1`
                echo "\n" >>results_d_test
                echo $name >>results_d_test
                paste -d" " a $i.b >data
                roc=`~/softwarekd/perf -roc < data | perl -pi -e 's/ROC//g' | perl -pi -e 's/ //g'`
                echo  "\tROC value\t$roc\n" >>results_d_test
                perl accuracy1_new.pl a $i.b results_d_test
                perl accuracy_new.pl a $i.b results_d_test
                 rm $i.b data
        done

