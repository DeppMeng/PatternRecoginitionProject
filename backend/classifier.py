import numpy as np

num_classes = 2
train_points = np.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]])
train_labels = np.array([0, 0, 0, 1, 1, 1], dtype=int)
test_points = np.array([[0, 0], [0, 1], [1, 1], [2, 1], [1, 0], [2, 0]])
test_labels = np.array([0, 0, 1, 1, 0, 0], dtype=int)

class Classifier:
    def __init__(self):
        self.num_classes = 2  # default as 2
        self.train_points = None
        self.train_labels = None
        self.test_points = None
        self.test_labels = None
        self.pred_labels = None # output predicted labels

        self.train_accuracy = 0
        self.test_accuracy = 0

        self.method = "min_dis"

        # minimum distance classifier
        self.central_points = None

    def _cal_accuracy(self, x, y):
        assert(x.shape==y.shape);
        cnt = 0
        for i in range(len(x)):
            if x[i] == y[i]:
                cnt += 1
        return cnt/len(x)

    def _dis_L2(self, x, y):
        d = x - y
        return np.sqrt(d[0] * d[0] + d[1] * d[1])

    def _load_train_data(self, train_points, train_labels, num_classes=None):
        assert (isinstance(train_points, np.ndarray) and len(train_points) >= 2)
        assert (isinstance(train_labels, np.ndarray) and len(train_labels) >= 2)
        assert (len(train_points) == len(train_labels))
        self.train_points = train_points
        self.train_labels = train_labels
        self.num_classes = max(self.train_labels) + 1
        assert (self.num_classes >= 2)
        if num_classes:
            assert (self.num_classes == num_classes)

    def predict(self, pred_points):
        try:
            # confirm that pred_points is in shape of (len, 2)
            assert (isinstance(pred_points, np.ndarray) and len(pred_points) > 0)
            assert (len(pred_points.shape) == 2 and pred_points.shape[1] == 2)
        except:
            print("Error: The pred_points is a point list, which should be in shape of (len, 2).")
        else:
            self.pred_labels = np.zeros(len(pred_points), dtype=int)
            if self.method == "min_dis":
                assert (isinstance(self.central_points, np.ndarray) and len(self.central_points) == self.num_classes)
                for idx in range(len(pred_points)):
                    dis = np.inf;
                    label = -1
                    for c in range(self.num_classes):
                        this_dis = self._dis_L2(pred_points[idx], self.central_points[c])
                        if this_dis < dis:
                            dis = this_dis
                            label = c
                    assert (label != -1)
                    self.pred_labels[idx] = label

    def train(self, train_points, train_labels, method="min_dis", num_classes=None):
        self._load_train_data(train_points, train_labels, num_classes=num_classes)
        self.method = method
        if self.method == "min_dis":
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

    def test(self, test_points, test_labels):
        assert(len(test_points) == len(test_labels))
        self.test_points = test_points
        self.test_labels = test_labels
        self.predict(self.test_points)
        self.test_accuracy = self._cal_accuracy(self.test_labels, self.pred_labels)



if __name__ == "__main__":
    classifier = Classifier()
    classifier.train(train_points, train_labels, method="min_dis")
    classifier.test(test_points, test_labels)
    classifier.predict(np.array([[0, 0]]))
    print (classifier.pred_labels[0])