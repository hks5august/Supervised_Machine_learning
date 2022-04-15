import sys
import numpy as np
import pandas as pd
from sklearn.grid_search import GridSearchCV
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

class EstimatorSelectionHelper:
    def __init__(self, models, params):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: %s" % missing_params)
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {}
    
    def fit(self, X, y, cv=10, n_jobs=1, verbose=1, scoring=None, refit=False):
        for key in self.keys:
            print("Running GridSearchCV for %s." % key)
            model = self.models[key]
            params = self.params[key]
            gs = GridSearchCV(model, params, cv=cv, n_jobs=n_jobs, 
                              verbose=verbose, scoring=scoring, refit=refit)
            gs.fit(X,y)
            self.grid_searches[key] = gs    
    
    def score_summary(self, sort_by='mean_score'):
        def row(key, scores, params):
            d = {
                 'estimator': key,
                 'min_score': min(scores),
                 'max_score': max(scores),
                 'mean_score': np.mean(scores),
                 'std_score': np.std(scores),
            }
            #return pd.Series(dict(params.items() + d.items()))
            return pd.Series({**params,**d})
                      
        rows = [row(k, gsc.cv_validation_scores, gsc.parameters) 
                     for k in self.keys
                     for gsc in self.grid_searches[k].grid_scores_]
        df = pd.concat(rows, axis=1).T.sort_values([sort_by], ascending=False)
        columns = ['estimator', 'min_score', 'mean_score', 'max_score', 'std_score']
        columns = columns + [c for c in df.columns if c not in columns]
        
        return df[columns]


from sklearn.ensemble import (ExtraTreesClassifier, RandomForestClassifier, 
                              AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.svm import SVC

models1 = { 
    'ExtraTreesClassifier': ExtraTreesClassifier(),
    'RandomForestClassifier': RandomForestClassifier(),
    'AdaBoostClassifier': AdaBoostClassifier(),
    'GradientBoostingClassifier': GradientBoostingClassifier(),
    'SVC': SVC(),
    'LR': LogisticRegression(),
    'Ridge Classifier': RidgeClassifier(),
    'Perceptron': Perceptron(),
    'knn': KNeighborsClassifier(),
    'svcl': LinearSVC(),
    'sgd' : SGDClassifier()
}

params1 = { 
    'ExtraTreesClassifier': { 'n_estimators': [10, 20,30,40,50] },
    'RandomForestClassifier': { 'n_estimators': [10,20,30,40,50,60,70,80,90] },
    'AdaBoostClassifier':  { 'n_estimators': [30,50,100] },
    'GradientBoostingClassifier': { 'n_estimators': [16, 32], 'learning_rate': [0.1,0.2,0.4,0.8, 1.0] },
    'SVC': [
        {'kernel': ['linear'], 'C': [1,2,3,4,5,6,7,8,9,10]},
        {'kernel': ['rbf'], 'C': [1,2,3,4,5,10], 'gamma': [1,0.5,0.01,0.001, 0.0001]}
    ],
    'Perceptron' : {'n_iter':[30,50,100,120]},
    'sgd':{'loss':['squared_hinge'],'penalty' : [ 'l2','l1']},
    'svcl':{'C': [1,2,3,4,5,10]},
    'LR' : {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]},
    'Ridge Classifier' : {'alpha' : [1,0.1,0.01,0.001,0.0001,0]},
    'knn' : {'n_neighbors':[5,6,7,8,9,10],'weights':['uniform', 'distance'],'algorithm':['auto', 'ball_tree','kd_tree','brute']}
}
filename = sys.argv[1]
# Build a classification task using 3 informative features
train=pd.read_csv(filename,index_col=0)
#X = train.loc[:, train.columns != 'flag']
X = train[train.columns[1:]]
y=train['flag']
helper1 = EstimatorSelectionHelper(models1, params1)
helper1.fit(X, y, scoring='roc_auc', n_jobs=-1)
type(helper1.score_summary(sort_by='mean_score'))
print(helper1.score_summary(sort_by='mean_score'))
helper1.score_summary(sort_by='mean_score').to_csv("parameters", sep='\t')
