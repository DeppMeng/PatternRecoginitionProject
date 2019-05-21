import math
import numpy as np

__all__ = ['Linear', 'Relu', 'CrossEntropyLoss']

class _Module:
    def __init__(self):
        self.training = True

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def backward(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def train(self):
        self.training = True

    def test(self):
        self.training = False

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)


class Linear(_Module):
    r"""Applies a linear transformation to the incoming data:
            y = Ax + b

       Args:
           in_features: size of each input sample
           out_features: size of each output sample`

       Shape:
           - Input:  (N, in_features)
           - Output:  (N, out_features)

       Attributes:
           weight: the learnable weights of the module of shape
                (out_features x in_features)
           bias:   the learnable bias of the module of shape
                (out_features)

       """

    def __init__(self, in_features, out_features):
        super(Linear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = np.empty((out_features, in_features))
        self.bias = np.empty(out_features)
        self.input = None
        self.grad_weight = None
        self.grad_bias = None
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1. / math.sqrt(self.weight.shape[1])
        self.weight = np.random.uniform(-stdv, stdv, self.weight.shape)
        self.bias = np.random.uniform(-stdv, stdv, self.bias.shape)

    def forward(self, input):
        if self.training:
            self.input = input
        return input @ self.weight.T + self.bias

    def backward(self, grad_output):
        grad_input = grad_output @ self.weight
        self.grad_weight = grad_output.T @ self.input
        self.grad_bias = grad_output.reshape(-1)
        return grad_input

    def update(self, lr):
        # print(self.grad_weight.shape)
        # print(self.weight.shape)
        self.weight -= lr * self.grad_weight
        self.bias -= lr * self.grad_bias
        self.input = None
        self.grad_weight = None
        self.grad_bias = None


class Relu(_Module):
    r"""Applies the rectified linear unit function element-wise
            x = max(0, x)

        Shape:
            - Input: (N, *) where `*` means, any number of additional
              dimensions
            - Output: (N, *), same shape as the input
        """

    def __init__(self):
        super(Relu, self).__init__()
        self.input = None

    def forward(self, input):
        if self.training:
            self.input = input
        return np.maximum(input, 0)

    def backward(self, grad_output):
        grad_input = grad_output.copy()
        grad_input[self.input < 0] = 0
        return grad_input

    def update(self, lr):
        self.input = None


class CrossEntropyLoss(_Module):
    def __init__(self):
        super(CrossEntropyLoss, self).__init__()
        self.target = None
        self.exp_input = None

    def forward(self, input, target):
        exp_input = np.exp(input)
        if self.training:
            self.target = target
            self.exp_input = exp_input
        loss = -np.take_along_axis(input, target, axis=1)+ np.log(exp_input.sum(1))

        loss = loss.mean()
        return loss

    def backward(self, grad_output):
        onehot_target = np.eye(self.exp_input.shape[1])[self.target.reshape(-1)]
        grad_input = grad_output * (self.exp_input/self.exp_input.sum() - onehot_target)
        return grad_input

    def update(self, lr):
        self.target = None
        self.exp_input = None

