import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = np.loadtxt("dataset.csv", dtype = np.float, delimiter=",",
                     usecols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
    target1 = np.loadtxt("dataset.csv", dtype=np.float, delimiter=",",
                     usecols=(15))

    target2 = np.loadtxt("dataset.csv", dtype=np.float, delimiter=",",
                     usecols=(14))
    print(data.shape)
    print(target1.shape)
    print(target2.shape)

    from sklearn import cross_validation

    train, test, t_train, t_test = cross_validation.train_test_split(data, target1, test_size=0.4, random_state=0)

    from pylab import plot, show

    plot(data[target1 == 0, 1], data[target1 == 0, 3], 'bo')
    plot(data[target1 == 1, 1], data[target1 == 1, 3], 'ro')
    show()

    from sklearn import metrics
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()

    model.fit(train, t_train)  # train

    expected = t_test
    predicted = model.predict(test)  ###

    print(model.predict(test))


    print(model.score(test, t_test))
      # test

    print(model.score(train, t_train))
    # test
    # 0.93333333333333335

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn import metrics
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn import metrics
    from sklearn.neighbors import KNeighborsClassifier  ####

    # fit a k-nearest neighbor model to the data
    model = KNeighborsClassifier()  ####

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn import metrics
    from sklearn.tree import DecisionTreeClassifier  ####

    # fit a CART model to the data
    model = DecisionTreeClassifier()  ####

    print(model)

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###
    print(expected)
    print(predicted)

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn import metrics
    from sklearn.svm import SVC  ####

    # fit a SVM model to the data
    model = SVC()  ####
    model.fit(train, t_train)

    print(model)

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier()  ####
    model.fit(train, t_train)

    print(model)

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn.ensemble import BaggingClassifier

    model = BaggingClassifier() ####
    model.fit(train, t_train)

    print(model)

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn.ensemble import AdaBoostClassifier

    model = AdaBoostClassifier()  ####
    model.fit(train, t_train)

    print(model)

    model.fit(train, t_train)

    expected = t_test
    predicted = model.predict(test)  ###

    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    from sklearn.linear_model import LinearRegression

    model = LinearRegression()

    model.fit(data, target2)

    print(model.coef_)
    predictions = {}
    predictions['intercept'] = model.intercept_
    predictions['coefficient'] = model.coef_

    print(predictions)

    # The mean square error
    np.mean((model.predict(data) - target2) ** 2)

