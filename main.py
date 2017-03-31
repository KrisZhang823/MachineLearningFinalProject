import pickle
import numpy
import random
import json
import sys
from PIL import Image


class QuadraticCost(object):
    @staticmethod
    def function(a, y):
        return 0.5*numpy.linalg.norm(a-y)**2

    @staticmethod
    def delta(z, a, y):
        return (a-y)*derivate_sigmod(z)


class CrossEntroyCost(object):
    @staticmethod
    def function(a, y):
        return -numpy.sum(numpy.nan_to_num(y*numpy.log(a)+(1-y)*numpy.log(1-a)))

    @staticmethod
    def delta(z, a, y):
        return a-y

class Network(object):
    def __init__(self, sizes, cost = CrossEntroyCost):
        self.length = len(sizes)
        self.sizes = sizes
        self.new_weights_initializer()
        self.cost = cost

    def new_weights_initializer(self):
        self.bias = [numpy.random.randn(y, 1) for y in self.sizes[1:]]
        self.weight = [numpy.random.randn(y, x)/numpy.sqrt(x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def original_weights_initializer(self):
        self.bias = [numpy.random.randn(y, 1) for y in self.sizes[1:]]
        self.weight = [numpy.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def freed_forward(self, a):
        for b, w in zip(self.bias, self.weight):
            a = sigmod(numpy.dot(w, a)+b)
        return a

    def sgd(self, tr_d, it_num, minibatch_size, eta, lmbda=0.0, evaluation_data=None,
            monitor_evaluation_cost=False,
            monitor_evaluation_accuracy=False,
            monitor_training_cost=False,
            monitor_training_accuracy=False):
        if evaluation_data:
            length = len(evaluation_data)
        n = len(tr_d)
        evaluation_cost, evaluation_accuracy = [], []
        training_cost, training_accuracy = [], []
        for j in range(it_num):
            random.shuffle(tr_d)
            minibatchs = [tr_d[k:k+minibatch_size] for k in range(0, n, minibatch_size)]
            for minibatch in minibatchs:
                self.update_mini_batch(minibatch, eta, lmbda, len(tr_d))
            print("Epoch {0} complete".format(j))
            if monitor_training_cost:
                cost = self.total_cost(tr_d, lmbda)
                training_cost.append(cost)
                print("Cost on training data: {}".format(cost))

            if monitor_training_accuracy:
                accuracy = self.evaluate(tr_d, convert=True)
                training_accuracy.append(accuracy)
                print("Accuracy on training data: {} / {}".format(accuracy, n))

            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                evaluation_cost.append(cost)
                print("Cost on evaluation data: {}".format(cost))

            if monitor_evaluation_accuracy:
                accuracy = self.evaluate(evaluation_data)
                evaluation_accuracy.append(accuracy)
                print("Accuracy on evaluation data: {} / {}".format(self.evaluate(evaluation_data), length))

        return evaluation_cost, evaluation_accuracy, \
               training_cost, training_accuracy

    def update_mini_batch(self, minibatch, eta, lmbda, n):
        nabla_b = [numpy.zeros(b.shape) for b in self.bias]
        nabla_w = [numpy.zeros(w.shape) for w in self.weight]
        for x, y in minibatch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weight = [(1-eta*(lmbda/n))*w-(eta/len(minibatch))*nw for w, nw in zip(self.weight,nabla_w)]
        self.bias = [b - eta/len(minibatch)*nb for b, nb in zip(self.bias, nabla_b)]

    def backprop(self, x, y):
        nabla_b = [numpy.zeros(b.shape) for b in self.bias]
        nabla_w = [numpy.zeros(w.shape) for w in self.weight]
        activation = x
        activations = [x]
        zs = []

        for b, w in zip(self.bias, self.weight):
            z = numpy.dot(w, activation) + b
            zs.append(z)
            activation = sigmod(z)
            activations.append(activation)

        delta = self.cost.delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = numpy.dot(delta, activations[-2].transpose())

        for l in range(2, self.length):
            z = zs[-l]
            sp = derivate_sigmod(z)
            delta = numpy.dot(self.weight[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = numpy.dot(delta, activations[-l - 1].transpose())

        return nabla_b, nabla_w

    def evaluate(self, data, convert=False):
        if convert:
            results = [(numpy.argmax(self.freed_forward(x)), numpy.argmax(y)) for (x, y) in data]
        else:
            results = [(numpy.argmax(self.freed_forward(x)), y) for (x, y) in data]
        return sum(int(x == y) for (x, y) in results)

    def total_cost(self, data, lmbda, convert=False):
        cost = 0.0
        for x, y in data:
            a = self.freed_forward(x)
            if convert : y = vectorize(y)
            cost += self.cost.function(a, y)/len(data)
        cost += 0.5*(lmbda/len(data))*sum(numpy.linalg.norm(w)**2 for w in self.weight)
        return cost

    def save_file(self, filename):
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weight],
                "biases": [b.tolist() for b in self.bias],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


def main():
    tr_d, va_d, t_d = reshape()
    net = Network([784, 30, 10])
    net.sgd(tr_d, 30, 10, 0.5, 5.0, va_d, True, True, True, True)
    net.save_file('the_data')


def load_file(filename):
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data['cost'])
    net = Network(data["sizes"], cost=cost)
    net.weights = [numpy.array(w) for w in data["weights"]]
    net.biases = [numpy.array(b) for b in data["biases"]]
    return net


def sigmod(z):
    return 1.0/(1.0+numpy.exp(-z))


def derivate_sigmod(z):
    return sigmod(z)*(1-sigmod(z))


def load_data(file_path="./mnist.pkl"):
    with open(file_path,'rb') as f:
        training_data, validation_data, test_data = pickle.load(f, encoding='bytes')
    # i = training_data[0][0]
    # i.resize((28,28))
    # im = Image.fromarray((I*256).astype('uint8'))
    # im.show()
    return training_data,validation_data,training_data


def reshape():
    tr_d, va_d, te_d = load_data()
    training_inputs = [numpy.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorize(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))
    validation_inputs = [numpy.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = list(zip(validation_inputs, va_d[1]))
    test_inputs = [numpy.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = list(zip(test_inputs, te_d[1]))
    return training_data, validation_data, test_data


def vectorize(j):
    y = numpy.zeros((10, 1))
    y[j] = 1
    return y


if __name__ == '__main__': main()
