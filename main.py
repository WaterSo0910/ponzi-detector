# %%
# Import
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from modules.Models import Classifier
import pandas as pd
import numpy as np
import re
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

# %% Set seeds
RANDOMSEED = 890104


# %%
# TODO: get all opcode list
with open("data/code/opcode_list.txt", 'r') as F:
    OPCODES_SET = set(F.read().split())

# TODO: read raw csv and their opcode
df = pd.read_csv("./data/code/ponzi.csv")

# %%
# TODO: preprocess opcode, remove first line, not exist field, numbers. Return List[str]


def opcodePreprocess(opcode: str):
    if not opcode.startswith("opcode"):
        return re.sub(r'[0-9]', '', opcode)
    else:
        return None


def ByteCodeReader(df: pd.DataFrame) -> Tuple[List[str], List[int]]:
    sentences: List[str] = []
    addrs: List[str] = df["addr"].tolist()
    labels: List[int] = df["IS_PONZI"].tolist()
    for addr in addrs:
        bytecode = []
        with open("./data/code/opcode/{}.txt".format(addr), 'r') as F:
            # Ignore first line
            for line in F.readlines()[1:]:
                operation: str = opcodePreprocess(line.split()[1])
                if operation != None:
                    bytecode.append(operation)
        sentences.append(' '.join(bytecode))
    return sentences, labels


sents, labels = ByteCodeReader(df)


# %%
# TODO: apply TFIDF vectorizer to get corpus
vectorizer = TfidfVectorizer(ngram_range=(1, 5))
X = vectorizer.fit_transform(sents)

# %%
# TODO: train test split  (80%,20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, stratify=labels, test_size=0.2, random_state=RANDOMSEED)


# %%
# Define models
models = {
    "RF": {
        "n_estimators": 120, "bootstrap": False, "criterion": "entropy", "random_state": RANDOMSEED,
    },
    "XGB": {
        "learning_rate": 0.2, "max_depth": 9, "n_estimators": 180, "seed": RANDOMSEED,
    },
    "SVM": {
        "random_state": RANDOMSEED,
    },
    "MLP": {
        "learning_rate": "adaptive", "random_state": RANDOMSEED
    },
}
# %%
# TODO: train & Validate
for name in models:
    model = Classifier(model_name=name, **models[name])
    # model.fit(X_train, y_train)
    model.load()
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print("==================================")
    print("- Validation Result of {}".format(model.name()))
    print("Accuracy : {}".format(acc))
    print("Precision: {}".format(precision))
    print("Recall   : {}".format(recall))
    print("F1-score : {}".format(f1))
    report = classification_report(y_test, y_pred)
    print(report)
    print("==================================")
    model.save()
