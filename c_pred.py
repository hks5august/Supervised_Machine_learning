# Compare Algorithms
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.feature_selection import RFE
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import ExtraTreesClassifier
import sys
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef
# load dataset
filename = sys.argv[1]
# Build a classification task using 3 informative features
train=pd.read_csv(filename,index_col=0)
#X = train.loc[:, train.columns != 'flag']
X = train[train.columns[1:]]
y=train['flag']
filename1 = sys.argv[2]
# Build a classification task using 3 informative features
test=pd.read_csv(filename1,index_col=0)
#X = train.loc[:, train.columns != 'flag']
X_test = test[test.columns[1:]]
y_test=test['flag']
# prepare configuration for cross validation test harness
seed = 7
# prepare models
models = []
#models.append(('LR', LogisticRegression(C=0.1)))
#models.append(('LR_w', LogisticRegression(C=0.1,class_weight="balanced")))
#models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('ETREES', ExtraTreesClassifier(n_estimators=20,class_weight="balanced")))
models.append(('NB', GaussianNB()))
#models.append(('Ridge Classifier',RidgeClassifier(tol=1e-2, solver="lsqr")))
#models.append(('Perceptron',Perceptron(n_iter=50)))
models.append(('knn',KNeighborsClassifier(n_neighbors=10)))
models.append(('RandomForest',RandomForestClassifier(n_estimators=80,class_weight="balanced")))
#models.append(('svc-l1',LinearSVC(loss='squared_hinge', penalty='l1', dual=False, tol=1e-3)))
#models.append(('svc-rbf',SVC(kernel="rbf",gamma=0.01,C=2,probability=True)))
#models.append(('svc-rbf',SVC(kernel="rbf",gamma=0.01,C=2,probability=True,class_weight="balanced")))
#models.append(('svc-l1_w',LinearSVC(loss='squared_hinge', penalty='l1', dual=False, tol=1e-3,class_weight="balanced")))
#models.append(('svc-l2',LinearSVC(loss='squared_hinge', penalty='l2', dual=False, tol=1e-3)))
#models.append(('sgd-l1',SGDClassifier(alpha=.0001, n_iter=50,penalty='l1')))
#models.append(('sgd-l2',SGDClassifier(alpha=.0001, n_iter=50,penalty='l2')))
#models.append(('sgd-elastic',SGDClassifier(alpha=.0001, n_iter=50,penalty='elasticnet')))
len=len(models)
# evaluate each model in turn
results = []
names = []
#scoring = 'roc_auc'
scoring = 'average_precision'
df = pd.DataFrame()
dft = pd.DataFrame()
df[1]=y
dft[1]=y_test
i=2
for name, model in models:
	kfold = model_selection.StratifiedKFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X, y, cv=kfold, scoring=scoring)
	cv_predict_results = model_selection.cross_val_predict(model, X, y, cv=kfold)
	cv_predict_results1 = model_selection.cross_val_predict(model, X, y, cv=kfold,method='predict_proba')
	y_pred_prob=[i[1] for i in cv_predict_results1]
	df[i]=y_pred_prob
	names.append(name)
	df.rename(columns ={i: name}, inplace =True)
	model.fit(X,y)
	pred_test1=model.predict_proba(X_test)
	y_pred_prob_test=[i[1] for i in pred_test1]
	dft[i]=y_pred_prob_test
	dft.rename(columns ={i: name}, inplace =True)
	i += 1
df.to_csv("train_rna_pred1")
dft.to_csv("test_rna_pred1") 
