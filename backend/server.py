from flask import Flask, request, jsonify
import json
from classifier import Classifier
import numpy as np

app = Flask(__name__)
LC = LinearClassifier()
NLC = MlpClassifier(num_layers=1, in_features=2, hidden_features=2, num_classes=2)
type_train_classifier = 0   # 0 is linear classifier, and 1 is nonlinear classifier

def unpack(package):
    '''
    # For example:
    package = [{"x": 0.084248461548879, "y": 0.4889971262375139, "label": 0.0},
               {"x": -0.085910405756836283, "y": 2.9155646782084554, "label": 1.0},
               {"x": -2.1217101421337463, "y": -1.22781866628299, "label": 0.0},
               {"x": 1.0532482381992037, "y": -0.20140028191871351, "label": 1.0}]
    '''
    points = []
    labels = []
    for i in range(len(package)):
        points.append([package[i]["x"], package[i]["y"]])
        labels.append(package[i]["label"])
    return np.array(points), np.array(labels, dtype=int)

def train(jsonpack):
    global type_train_classifier
    train_points, train_labels = unpack(jsonpack['traindata'])
    if jsonpack['classifiertype'] == 0:
        type_train_classifier = 0
        LC.train(train_points, train_labels, method='min_dis')
        result = {
            "train_accuracy": LC.train_accuracy,
            "pred_labels": LC.pred_labels
        }
    else:
        type_train_classifier = 1
        NLC.train(train_points, train_labels, total_epochs=1000, lr=1.0)
        result = {
            "train_accuracy": NLC.train_accuracy,
            "pred_labels": NLC.pred_labels
        }
    return result

def test(jsonpack):
    test_points, test_labels = unpack(jsonpack['testdata'])
    if jsonpack['classifiertype'] == 0:
        assert(type_train_classifier == 0)
        LC.test(test_points, test_labels)
        result = {
            "test_accuracy": LC.test_accuracy,
            "pred_labels": LC.pred_labels
        }
    else:
        assert (type_train_classifier == 1)
        NLC.test(test_points, test_labels)
        result = {
            "test_accuracy": NLC.test_accuracy,
            "pred_labels": NLC.pred_labels
        }
    return result

def predict(jsonpack):
    pred_points, _ = unpack(jsonpack['testdata'])
    if jsonpack['classifiertype'] == 0:
        assert(type_train_classifier == 0)
        LC.predict(pred_points)
        print(LC.pred_labels)
        result = {
            "pred_labels": LC.pred_labels
        }
    else:
        assert (type_train_classifier == 1)
        NLC.predict(pred_points)
        print(NLC.pred_labels)
        result = {
            "pred_labels": NLC.pred_labels
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