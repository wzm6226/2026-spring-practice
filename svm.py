import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_blobs, load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

def toy_data():#手动生成简单二维数据
    X = np.array([[0,1],[1, 2], [2, 3], [3, 4], [4, 6]])
    y = np.array([0, 0, 0,1,1])
    return X, y

def random_data():#生成随机聚类数据
    X, y = make_blobs(n_samples=100, centers=2, random_state=42)
    return X, y

def iris_data():#鸢尾花数据集
    iris = load_iris()
    X, y = iris.data[:, :2], iris.target
    return X, y

def plot_decision_boundary(X, y, clf):
    plt.figure(figsize=(10, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=100)
    
    ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 50),
                         np.linspace(ylim[0], ylim[1], 50))
    
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
                linestyles=['--', '-', '--'])
    
    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=200,
                linewidth=1, facecolors='none', edgecolors='k')
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('SVM Decision Boundary')
    plt.show()

def experiment(X, y, kernel='linear', C=1.0):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    if kernel == 'linear':
        clf = SVC(kernel='linear', C=C)
    elif kernel == 'poly':
        clf = SVC(kernel='poly', degree=3, C=C) 
    elif kernel == 'rbf':
        clf = SVC(kernel='rbf', C=C) 
    else:
        raise ValueError("Invalid kernel type. Choose from 'linear', 'poly', or 'rbf'.")
    
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print(f"Accuracy with kernel={kernel}, C={C}: {score}")
    return clf

def main():
    datasets = [toy_data(), random_data(), iris_data()]
    for X, y in datasets:
        print("Experimenting with dataset:")
        if X.shape[1] == 2:
            print("Visualization available")
            kernels = ['linear', 'poly', 'rbf']  
            for kernel in kernels:
                print(f"Kernel: {kernel}")
                clf = experiment(X, y, kernel=kernel, C=1.0)
                plot_decision_boundary(X, y, clf)
        else:
            print("Visualization not available for this dataset")
        print("===================================")

if __name__ == "__main__":
    main()
