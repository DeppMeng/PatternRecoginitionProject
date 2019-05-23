import pickle
import numpy as np
from layer import *

num_classes = 2
train_points = np.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]])
train_labels = np.array([0, 0, 0, 1, 1, 1], dtype=int)
test_points = np.array([[0, 0], [0, 1], [1, 1], [2, 1], [1, 0], [2, 0]])
test_labels = np.array([0, 0, 1, 1, 0, 0], dtype=int)


def save_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)


def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


def get_classifier(method, **kwargs):
    if method == 'min_dis':
        return LinearClassifier()
    elif method == 'mlp':
        return MlpClassifier(num_layers=kwargs['num_layer'],
                             in_features=kwargs['in_features'],
                             hidden_features=kwargs['hidden_features'],
                             num_classes=kwargs['num_classes'])

class _BaseClassifier:
    def __init__(self):
        self.num_classes = 2  # default as 2
        self.refresh()

    def refresh(self):
        self.train_points = None
        self.train_labels = None
        self.test_points = None
        self.test_labels = None
        self.pred_labels = None   # output predicted labels
        self.train_accuracy = 0
        self.test_accuracy = 0

    def train(self, train_points, train_labels, *args, **kwargs):
        raise NotImplementedError

    def test(self, *args, **kwargs):
        raise NotImplementedError

    def predict(self, *args, **kwargs):
        raise NotImplementedError

    def _cal_accuracy(self, x, y):
        assert(x.shape==y.shape);
        cnt = 0
        for i in range(len(x)):
            if x[i] == y[i]:
                cnt += 1
        return cnt/len(x)

    def _shuffle_train_data(self):
        shuffle = np.random.permutation(self.train_points.shape[0])
        self.train_points = self.train_points[shuffle]
        self.train_labels = self.train_labels[shuffle]

    def _load_train_data(self, train_points, train_labels, num_classes=None):
        assert (isinstance(train_points, np.ndarray) and len(train_points) >= 2)
        assert (isinstance(train_labels, np.ndarray) and len(train_labels) >= 2)
        assert (len(train_points) == len(train_labels))
        self.train_points = train_points
        self.train_labels = train_labels
        self.num_classes = max(self.train_labels) + 1
        assert (self.num_classes >= 2)
        # print(self.num_classes)
        # print(num_classes)
        if num_classes:
            assert (self.num_classes == num_classes)


class LinearClassifier(_BaseClassifier):
    def __init__(self):
        super(LinearClassifier, self).__init__()
        self.method_list = []

        # minimum distance classifier
        self.central_points = None

    def _dis_L2(self, x, y):
        d = x - y
        return np.sqrt(d[0] * d[0] + d[1] * d[1])

    def predict(self, pred_points, method='min_dis'):
        try:
            # confirm that pred_points is in shape of (len, 2)
            assert (isinstance(pred_points, np.ndarray) and len(pred_points) > 0)
            assert (len(pred_points.shape) == 2 and pred_points.shape[1] == 2)
            # confirm that predict method is in self.method_list
            assert method in self.method_list
        except:
            print("Error: The pred_points is a point list, which should be in shape of (len, 2).")
        else:
            self.pred_labels = np.zeros(len(pred_points), dtype=int)
            if method == "min_dis":
                assert (isinstance(self.central_points, np.ndarray) and len(self.central_points) == self.num_classes)
                for idx in range(len(pred_points)):
                    dis = np.inf
                    label = -1
                    for c in range(self.num_classes):
                        this_dis = self._dis_L2(pred_points[idx], self.central_points[c])
                        if this_dis < dis:
                            dis = this_dis
                            label = c
                    assert (label != -1)
                    self.pred_labels[idx] = label

    def train(self, train_points, train_labels, method="min_dis", num_classes=None, **kwargs):
        self._load_train_data(train_points, train_labels, num_classes=num_classes)
        # register new method
        if method not in self.method_list:
            self.method_list.append(method)

        if method == "min_dis":
            self.central_points = np.zeros((self.num_classes, 2))
            for c in range(self.num_classes):
                sum = np.zeros(2)
                cnt = 0
                for idx in range(len(self.train_points)):
                    if self.train_labels[idx] == c:
                        sum += self.train_points[idx]
                        cnt += 1
                self.central_points[c] = sum / cnt
        self.predict(self.train_points)
        self.train_accuracy = self._cal_accuracy(self.train_labels, self.pred_labels)

    def test(self, test_points, test_labels, method='min_dis'):
        assert(len(test_points) == len(test_labels))
        self.test_points = test_points
        self.test_labels = test_labels
        self.predict(self.test_points, method=method)
        self.test_accuracy = self._cal_accuracy(self.test_labels, self.pred_labels)


class MlpClassifier(_BaseClassifier):
    def __init__(self, num_layers, in_features, hidden_features, num_classes):
        super(MlpClassifier, self).__init__()
        self.nlayer = num_layers
        self.in_features = in_features
        self.hidden_features = hidden_features
        self.num_classes = num_classes

        if self.nlayer == 1:
            self.module = [Linear(in_features, num_classes)]
        else:
            self.module = [Linear(in_features, hidden_features),
                           Relu()]
            for _ in range(num_layers - 2):
                self.module += [Linear(hidden_features, hidden_features),
                                Relu()]
            self.module += [Linear(hidden_features, num_classes)]
        self.LossLayer = CrossEntropyLoss()

    def forward(self, x):
        for layer in self.module:
            x = layer(x)
        return x

    def backward(self):
        grad = self.LossLayer.backward(1)
        for i in range(len(self.module) - 1, -1, -1):
            grad = self.module[i].backward(grad)

    def update(self, lr):
        for layer in self.module:
            layer.update(lr)
        self.LossLayer.update(lr)

    def predict(self, pred_points, ):
        try:
            # confirm that pred_points is in shape of (len, self.in_features)
            assert (isinstance(pred_points, np.ndarray) and len(pred_points) > 0)
            assert (len(pred_points.shape) == 2 and pred_points.shape[1] == self.in_features)
        except:
            print("Error: The pred_points is a point list, which should be in shape of (len, 2).")
        else:
            pred_scores = self.forward(pred_points)
            self.pred_labels = np.argmax(pred_scores, axis=1)

    def train(self, train_points, train_labels, total_epochs=1000, num_classes=None, lr=0.1, batch_size=1, **kwargs):
        self._load_train_data(train_points, train_labels, num_classes=num_classes)
        N = self.train_labels.shape[0]
        for epoch in range(total_epochs):
            epoch_loss = 0
            self._shuffle_train_data()
            for step in range(N):
                data = self.train_points[step: step + batch_size]
                target = self.train_labels.reshape(-1, 1)[step: step + batch_size]
                pred_scores = self.forward(data)
                loss = self.LossLayer(pred_scores, target)
                self.backward()
                self.update(lr)
                epoch_loss += loss

            self.predict(self.train_points)
            self.train_accuracy = self._cal_accuracy(self.train_labels, self.pred_labels)
            print("Epoch [{}/{}], Loss: {:.6f}, TrainAcc: {}".format(epoch, total_epochs, epoch_loss/N, self.train_accuracy))

    def test(self, test_points, test_labels):
        assert(len(test_points) == len(test_labels))
        self.test_points = test_points
        self.test_labels = test_labels
        self.predict(self.test_points)
        self.test_accuracy = self._cal_accuracy(self.test_labels, self.pred_labels)


if __name__ == "__main__":
    classifier = LinearClassifier()
    # classifier = get_classifier(method='min_dis')
    classifier.train(train_points, train_labels, method="min_dis")
    classifier.test(test_points, test_labels)
    classifier.predict(np.array([[0, 0]]))
    print (classifier.pred_labels[0])
    classifier.refresh()
    save_model(classifier, 'temp/model.pkl')
    # classifier = load_model('temp/model.pkl')
    # classifier.predict(np.array([[0, 0]]))
    # print(classifier.pred_labels[0])

    # classifier = MlpClassifier(num_layers=2,
    #                            in_features=2,
    #                            hidden_features=10,
    #                            num_classes=2)
    # classifier.train(train_points, train_labels, total_epochs=1000, lr=0.1, batch_size=1)
    # classifier.test(test_points, test_labels)
    # classifier.predict(np.array([[0, 0]]))
    # print(classifier.pred_labels[0])