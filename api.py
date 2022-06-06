from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
from flask import request
from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
        line = row.split()
        if len(line)==0: continue
        token = opcodePreprocess(row.split()[0])
        if token!=None:
            sents.append(token)
    X = VEC.transform([' '.join(sents)])
    prob = Model.predict_proba(X)
    if prob[0][0]>prob[0][1]:
        return 0, prob[0][0].item()
    else:
        return 1, prob[0][1].item()

@app.route("/api/ponzi",methods=['POST'])
@cross_origin()
def hello_world():
    opcode = request.stream.read().decode("utf-8")
    result,prob = Vectorize(opcode)
    return {
        "label":result,
        "prob":prob
    }

if __name__ == "__main__":
    app.run(debug=True)