import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):
    # 1. Format the data
    num_examples = len(x_train)
    batch_size = 200
    full_set = (int) (num_examples / batch_size)
    losses = np.zeros(epoch)
    # 2. call four_nn function to obtain losses
    for e in range(epoch):
        print(e)
        # if shuffle:
        #     #np.random.seed(seed=57)
        #     np.random.shuffle(x_train)
        #     np.random.shuffle(y_train)

        total_loss = 0
        for i in range(full_set):
            X, y = x_train[i * batch_size: i * batch_size + batch_size], y_train[i * batch_size: i * batch_size + batch_size]
            loss, w1, w2, w3, w4 = four_nn(X, w1, w2, w3, w4, b1, b2, b3, b4, y, False)
            total_loss += loss
        losses[e] = total_loss
    # 3. Return all the weights/biases and a list of losses at each epoch
    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):

    class_rate_per_class = [0.0] * num_classes
    avg_class_rate = 0

    size_per_class = 0
    for class_type in y_test:
        if class_type == 1:
            size_per_class += 1

    classifications = four_nn(x_test, w1, w2, w3, w4, b1, b2, b3, b4, y_test, True)
    for i in range(len(x_test)):
        if classifications[i] == y_test[i]:
            class_rate_per_class[y_test[i]] += 1
            avg_class_rate += 1

    avg_class_rate /= len(x_test)
    for i in range(len(class_rate_per_class)):
        class_rate_per_class[i] /= size_per_class

    class_names = np.array(["0","1","2","3","4","5","6","7","8","9"])
    plot_confusion_matrix(y_test, classifications, classes=class_names, normalize=True,
                      title='MNIST 4-Layer NN Confusion Matrix (50 Epoch)')
    plt.show()

    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(X, w1, w2, w3, w4, b1, b2, b3, b4, y,test):
    learning_rate = 0.1

    Z1, acache1 = affine_forward(X,w1,b1)
    A1, rcache1 = relu_forward(Z1)
    Z2, acache2 = affine_forward(A1,w2,b2)
    A2, rcache2 = relu_forward(Z2)
    Z3, acache3 = affine_forward(A2,w3,b3)
    A3, rcache3 = relu_forward(Z3)
    F, acache4 = affine_forward(A3,w4,b4)

    # return classifications = argmax over all classes in logits for each example
    if test:
        return [np.argmax(x) for x in F]

    loss, dF = cross_entropy(F,y)
    dA3, dW4, db4 = affine_backward(dF, acache4)
    dZ3 = relu_backward(dA3, rcache3)
    dA2, dW3, db3 = affine_backward(dZ3,acache3)
    dZ2 = relu_backward(dA2, rcache2)
    dA1, dW2, db2 = affine_backward(dZ2,acache2)
    dZ1 = relu_backward(dA1, rcache1)
    dX, dW1, db1 = affine_backward(dZ1,acache1)

    # use gradient descent to update parameters W1 = w1 - n dW1
    w1 -= learning_rate * dW1
    w2 -= learning_rate * dW2
    w3 -= learning_rate * dW3
    w4 -= learning_rate * dW4

    return loss, w1, w2, w3, w4

"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    Z = np.matmul(A, W) + b
    cache = (A, W, b)
    return Z, cache

def affine_backward(dZ, cache):
    A = cache[0]
    W = cache[1]
    b = cache[2]
    dA = np.matmul(dZ, W.T)
    dW = np.matmul(A.T, dZ)
    dB = sum(dZ)
    return dA, dW, dB

def relu_forward(Z):
    A = Z.copy()
    cache = Z
    A[A <= 0] = 0
    return A, cache

def relu_backward(dA, cache):
    Z = cache.copy()
    dZ = dA.copy()
    dZ[Z <= 0] = 0
    return dZ

def cross_entropy(F, y):
    loss = 0
    fy_total_i = 0
    dF = F.copy()
    for i in range(F.shape[0]):
        loss += F[i, int(y[i])]
        f_total = 0
        for k in range(F.shape[1]):
            f_total += np.exp(F[i, k])
            sum_exp = sum(np.exp(F[i, :]))
            binary = k == y[i]
            dF[i, k] = binary - np.exp(F[i, k]) / sum_exp
            dF[i, k] /= (-1 * F.shape[0])
        loss -= np.log(f_total)
    loss /= -F.shape[0]

    return loss, dF
