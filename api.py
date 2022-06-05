from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
from flask import request
from flask import Flask

app = Flask(__name__)

with open("data/code/opcode_list.txt", 'r') as F:
    OPCODES_SET = set(F.read().split())

with open('./pickle/vec.pkl', 'rb') as f:
    VEC:TfidfVectorizer = pickle.load(f)

with open('./pickle/MLPClassifier.pkl', 'rb') as f:
    Model:MLPClassifier = pickle.load(f)

def opcodePreprocess(opcode: str):
    if opcode in OPCODES_SET:
        return re.sub(r'[0-9]', '', opcode)
    else:
        return None

def Vectorize(text:str):
    sents = []
    for row in text.split("\n"):
        token = opcodePreprocess(row.split()[0])
        if token!=None:
            sents.append(token)
    X = VEC.transform([' '.join(sents)])
    y_pred = Model.predict(X)
    return y_pred[0].item()

@app.route("/api/ponzi",methods=['POST'])
def hello_world():
    opcode = request.stream.read().decode("utf-8")
    result = Vectorize(opcode)
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)