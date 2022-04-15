rm results results_*
~/anaconda3/bin/python c_pred.py new_sel_train new_sel_test
wait
 ~/anaconda3/bin/python c_pred_decision.py new_sel_train new_sel_test
wait
sh s.sh
sh s_decision.sh
paste results results_t >p
paste results_d results_d_test >d
cat p d >final_results
