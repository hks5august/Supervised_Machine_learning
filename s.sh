cut -d, -f2- train_rna_pred1 >ss
perl -i -pe   's/^1,/+1,/g' ss 
perl -i -pe  's/^0,/-1,/g' ss
cut -d, -f1 ss |tail -n+2 >a
for i in `seq 2 5`;
        do
         	echo $i|cut -d, -f$i ss |tail -n+2 >$i.b
         	name=`echo $i|cut -d, -f$i ss |head -1`
         	echo "\n" >>results
         	echo $name>>results
	 	paste -d" " a $i.b >data
	 	roc=`~/softwarekd/perf -roc < data | perl -pi -e 's/ROC//g' | perl -pi -e 's/ //g'`
	 	echo  "\tROC value\t$roc\n" >>results
	 	perl accuracy_new.pl a $i.b results
		rm $i.b data
	done   



cut -d, -f2- test_rna_pred1 >ss
perl -i -pe   's/^1,/+1,/g' ss
perl -i -pe  's/^0,/-1,/g' ss
cut -d, -f1 ss |tail -n+2 >a
for i in `seq 2 5`;
        do
                echo $i|cut -d, -f$i ss |tail -n+2 >$i.b
                name=`echo $i|cut -d, -f$i ss |head -1`
                echo "\n" >>results_t
                echo $name>>results_t
                paste -d" " a $i.b >data
                roc=`~/softwarekd/perf -roc < data | perl -pi -e 's/ROC//g' | perl -pi -e 's/ //g'`
                echo  "\tROC value\t$roc\n" >>results_t
                perl accuracy_new.pl a $i.b results_t
                rm $i.b data
        done

