from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_train = X.shape[0]
    num_classes = W.shape[1]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    for i in range(num_train):
      scores = X[i].dot(W)
      scores -= np.max(scores)
      logits = np.exp(scores)
      logits_sum = np.sum(logits)
      softmax_prob = logits/logits_sum
      loss += -np.log(softmax_prob[y[i]])
      for j in range(num_classes):
        if j == y[i]:
          dW[:, j] += (softmax_prob[j] - 1) * X[i]
        else:
          dW[:,j] += softmax_prob[j] * X[i]
      
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    loss /= num_train
    loss += reg * np.sum(W*W)
    dW /= num_train
    dW += 2* reg * W

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_train = X.shape[0]
    num_classes = W.shape[1]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    scores = X.dot(W)
    scores = np.subtract(scores,(np.max(scores, axis = 1)[:,np.newaxis]))
    logits = np.exp(scores)
    logits_sum = np.sum(logits, axis = 1)
    softmax_prob = np.divide(logits,logits_sum[:,np.newaxis])
    loss = -np.log(softmax_prob[(np.arange(num_train)),y])
    loss = np.sum(loss) / num_train
    loss += reg * np.sum(W*W)
    softmax_prob[(np.arange(num_train)),y] -= 1
    dW = X.T.dot(softmax_prob)
    dW /= num_train
    dW += 2 * reg * W


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
