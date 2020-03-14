from math import *
import copy
import collections
import string


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.probability_w = []
        self.words = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X-список сообщени1, y-классы, правильные ответы для Х сообщений. """
        X_copy = []
        for i in X:
            k = i.translate(str.maketrans("", "", string.punctuation))
            X_copy.append(k.lower().split())
        dict_never = collections.Counter()
        dict_good = collections.Counter()
        dict_maybe = collections.Counter()
        dict_all = collections.Counter()
        for i in range(len(X_copy)):
            for word in X_copy[i]:
                if word != '':
                    dict_all[word] += 1
                    if y[i] == 'good':
                        dict_good[word] += 1
                    elif y[i] == 'maybe':
                        dict_maybe[word] += 1
                    else:
                        dict_never[word] += 1
        for word in dict_all:
            prob = []
            prob.append((dict_good[word] + self.alpha) / (len(dict_good) + self.alpha * len(dict_all)))
            prob.append((dict_maybe[word] + self.alpha) / (len(dict_maybe) + self.alpha * len(dict_all)))
            prob.append((dict_never[word] + self.alpha) / (len(dict_never) + self.alpha * len(dict_all)))
            self.probability_w.append(prob)
            self.words.append(word)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. аозвращает У """
        X_copy = []
        for i in X:
            k = i.translate(str.maketrans("", "", string.punctuation))
            X_copy.append(k.lower().split())
        prob_news = []
        for i in enumerate(X_copy):
            prob_new = [log(1/3), log(1/3), log(1/3)]
            for word in i[1]:
                if word != '':
                    if word in self.words:
                        index_w = self.words.index(word)
                        prob_new[0] += log(self.probability_w[index_w][0])
                        prob_new[1] += log(self.probability_w[index_w][1])
                        prob_new[2] += log(self.probability_w[index_w][2])
            prob_news.append(prob_new.index(max(prob_new)))
        label = []
        for i in prob_news:
            if i == 0:
                label.append('good')
            elif i == 1:
                label.append('maybe')
            else:
                label.append('never')
        return label

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels.y_test-правильные """
        prediction = self.predict(X_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        value = count / len(y_test)
        return value

