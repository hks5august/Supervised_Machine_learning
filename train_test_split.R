############# train and test data split ##########
#####split protein data #########
args <- commandArgs(TRUE)
data_pro<- read.table (args[1], header=T, sep="\t", row.names = 1)
pro_names<-colnames(data_pro)
n<-length(pro_names)
indexes1 = sample(1:nrow(data_pro), size=0.2*nrow(data_pro))
 # Split data
test_pro = data_pro[indexes1,]
write.table(test_pro, file = "test",sep='\t', quote=F)
train_pro = data_pro[-indexes1,]
write.table(train_pro, file = "train", sep='\t', quote=F)

