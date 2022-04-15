#Store features in a vaiable as features
features <- varImpPlot(rforest, main='Feature Importance', pch=1, cex=0.6)


#Write features in a txt file format
write.table(features,'features_importance.txt', row.names=TRUE,col.names=NA, sep='\t', quote=FALSE)

# Sort features based on meandecrease accuracy value
sorted_features <- as.data.frame(features[order(features[,"MeanDecreaseAccuracy"], decreasing = TRUE),])

#select only top features (meanDecreaseaccuracy >1.5)
top_features <- sorted_features[sorted_features$MeanDecreaseAccuracy>1.5, ]

top1 <- as.data.frame(row.names(top_features))
#add class column as well
top1<-rbind(c("class"), top1)

colnames(top1) <- c("ID")

#Read full data
full_data <- read.table("https://code.omicslogic.com/assets/datasets/cell_lines/CellLines_52samples_ExprData_T1.txt", sep='\t', header=TRUE, stringsAsFactors=FALSE)

# Prepare data with only selected top features
selected_data <- as.data.frame(full_data[ full_data$id %in% c(top1$ID), ])

selected_data_t <- as.data.frame(t(selected_data))

colnames(selected_data_t)<-NULL


#Write selected data in a txt file
write.table(selected_data,'selected_data.txt', row.names=F,  sep='\t', quote=FALSE)

#Write selected data in a txt file
write.table(selected_data_t,'selected_data_transposed.txt', row.names=T, col.names=F, sep='\t', quote=FALSE)



pca_input <- read.table("selected_data_transposed.txt", sep="\t", header=TRUE,  row.names=1)
dim(pca_input)
tail(pca_input)

df <- as.matrix(pca_input[2:111])

pca_res <- prcomp(df)


plot(pca_res$x, pca_res$y)


















library(ggfortify)

pca_input <- read.table("https://raw.githubusercontent.com/pine-bio-support/Predictive_model_Classification_Regression/main/selected_data_transposed.txt", sep="\t", header=TRUE,  row.names=1)
dim(pca_input)
#head(pca_input)

df <- as.matrix(pca_input[2:ncol(pca_input)])
head(df)

#create PCA object
pca_res <- prcomp(df)

pca_res$x[1:10]
