from flask import Flask, request, jsonify
import json
from classifier import Classifier
app = Flask(__name__)

classifier = Classifier() # To confirm: global variable should be defined here?

def train(jsonpack):
    train_points = jsonpack['train_points']
    train_labels = jsonpack['train_labels']
    method = 'min_dis'
    if jsonpack['method']:
        method = jsonpack['method']
    classifier.train(train_points, train_labels, method=method)
    result = {
        "train_accuracy": classifier.train_accuracy,
        "pred_labels": classifier.pred_labels
    }
    return result

def test(jsonpack):
    test_points = jsonpack['test_points']
    test_labels = jsonpack['test_labels']
    classifier.test(test_points, test_labels)
    result = {
        "test_accuracy": classifier.test_accuracy,
        "pred_labels": classifier.pred_labels
    }
    return result

def predict(jsonpack):
    pred_points = jsonpack['pred_points']
    classifier.predict(pred_points)
    print(classifier.pred_labels)
    result = {
        "pred_labels": classifier.pred_labels
    }
    return result

POST_FUNCS = {
    "Train": train,
    "Test": test,
    "Predict": predict
}


@app.route('/post', methods=['POST'])
def post():

    jsonpack = request.json

    rtype = jsonpack['request_type']

    if rtype in POST_FUNCS:
        return jsonify(POST_FUNCS[rtype](jsonpack))
    return jsonify('')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)