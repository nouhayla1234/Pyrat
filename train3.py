from sklearn.ensemble import RandomForestClassifier
from sklearn.manifold import Isomap
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import svm

import numpy as np
import random as rd
import pickle
from sklearn.externals import joblib
mazeWidth = 21
mazeHeight = 15

import pickle, scipy


x,y = pickle.load(open("pyrat_dataset.pkl","rb"))
x = scipy.sparse.vstack(x).todense()
y = scipy.sparse.vstack(y).todense()

x = np.array(x).reshape(-1,(2*mazeHeight-1)*(2*mazeWidth-1))
y = np.argmax(np.array(y),1)


#iso = Isomap(n_neighbors=10,n_components=30)
#proj = iso.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=1)
svml = svm.NuSVC()
svml.fit(x_train,y_train)
print(svml.score(x_train,y_train),svml.score(x_test,y_test))

joblib.dump(svml,'save6.pkl') 
