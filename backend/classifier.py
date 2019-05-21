import numpy as np

num_classes = 2
train_points = np.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]])
train_labels = np.array([0, 0, 0, 1, 1, 1], dtype=int)
test_points = np.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]])


class Classifier:
    def __init__(self):
        self.num_classes = 2  # default as 2
        self.train_points = None
        self.train_labels = None
        self.test_points = None
        self.test_labels = None
        self.method = "min_dis"

        # minimum distance classifier
        self.standard_points = None

    def load_train_data(self, train_points, train_labels, num_classes=None):
        assert (len(train_points) == len(train_labels))
        self.train_points = train_points
        self.train_labels = train_labels
        self.num_classes = max(self.train_labels) + 1
        if num_classes:
            assert (self.num_classes == num_classes)

    def train(self, method="min_dis"):
        assert (isinstance(self.train_points, np.ndarray) and len(self.train_points) >= 2)
        assert (isinstance(self.train_labels, np.ndarray) and len(self.train_labels) >= 2)
        assert (self.num_classes >= 2)
        self.method = method
        if self.method == "min_dis":
            self.standard_points = np.zeros((self.num_classes, 2))
            for c in range(self.num_classes):
                sum = np.zeros(2)
                cnt = 0
                for idx in range(len(self.train_points)):
                    if self.train_labels[idx] == c:
                        sum += self.train_points[idx]
                        cnt += 1
                self.standard_points[c] = sum / cnt

    def _dis_L2(self, x, y):
        d = x - y
        return np.sqrt(d[0] * d[0] + d[1] * d[1])

    def test(self, test_points):
        try:
            assert (isinstance(test_points, np.ndarray) and len(test_points) > 0)
            assert (len(test_points.shape) == 2 and test_points.shape[1] == 2)
        except:
            print("Error: The test_points is a point list, which should be in shape of (len, 2).")
        else:
            self.test_points = test_points
            self.test_labels = np.zeros(len(self.test_points), dtype=int)
            if self.method == "min_dis":
                assert (isinstance(self.standard_points, np.ndarray) and len(self.standard_points) == self.num_classes)
                for idx in range(len(self.test_points)):
                    dis = np.inf;
                    label = -1
                    for c in range(self.num_classes):
                        this_dis = self._dis_L2(self.test_points[idx], self.standard_points[c])
                        if this_dis < dis:
                            dis = this_dis
                            label = c
                    assert (label != -1)
                    self.test_labels[idx] = label


if __name__ == "__main__":
    classifier = Classifier()
    classifier.load_train_data(train_points, train_labels)
    classifier.train("min_dis")
    classifier.test(test_points)
