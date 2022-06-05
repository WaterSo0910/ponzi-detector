from sklearn.ensemble import RandomForestClassifier,IsolationForest
from xgboost.sklearn import XGBClassifier
from sklearn.svm import SVC
from typing import Any
from sklearn.neural_network import MLPClassifier
import pickle

__model_dict__ = {
    "RF": RandomForestClassifier,
    "XGB": XGBClassifier,
    "IF":IsolationForest,
    "SVM":SVC,
    "MLP":MLPClassifier,
}


class Classifier:
    def __init__(self, model_name: str, **kwargs) -> None:
        assert model_name in __model_dict__.keys(), "Expected model_name in {}".format(list(__model_dict__.keys()))
        self.model_name = __model_dict__[model_name].__name__
        self.model = __model_dict__[model_name](**kwargs)

    def name(self)->str:
        return  self.model_name

    def fit(self, X: Any, y: Any):
        self.model.fit(X, y)

    def predict(self, data: Any):
        return self.model.predict(data)

    def save(self):
        with open('./pickle/{}.pkl'.format(self.name()),'wb') as f:
            pickle.dump(self.model,f)

    def load(self):
        with open('./pickle/{}.pkl'.format(self.name()), 'rb') as f:
            self.model = pickle.load(f)
