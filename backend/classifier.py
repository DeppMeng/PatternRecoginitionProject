import numpy as np
num_classes = 2
dim_input = 2

train_sample = np.array([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]])
train_label = np.array([0, 0, 0, 1, 1, 1], dtype=int)
test_data = np.array([-1, 0])




class TrainData:
    def __init__(self):

    def load_data(self, train_sample, train_label):
        self.train_sample = train_sample
        self.train_label = train_label
    

def min_dis_classifier(train_data, test_data, num_classes, dim_input, method="average_sample"):
    M = np.zeros((num_classes, dim_input))
    num_sample_in_class = np.zeros(num_classes)
    num_sample = np.size(train_data.train_label)
    if method == "average_sample":
        for i in range(num_sample):
            num_sample_in_class[train_data.train_label[i]] += 1
        for i in range(num_sample):
            curr_class = train_data.train_label[i]
            M[curr_class, :] += train_data.train_sample[i] / num_sample_in_class[curr_class]
    
    G = np.matmul(M, test_data) + np.matmul(M, np.transpose(M))
    result = np.argmax(G)
    return result


    



if __name__ == "__main__":
    train_data = TrainData()
    train_data.load_data(train_sample, train_label)

    result = min_dis_classifier(train_data, test_data)
