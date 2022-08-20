from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix,accuracy_score, classification_report
import pandas as pd
import argparse
import pickle
def training(input):
    data = pd.read_csv(input)
    X = data["Feed"]
    y = data["Sentiment"]

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size =.2, random_state=100)

    # make pipeline
    pipe = make_pipeline(TfidfVectorizer(),
                        LogisticRegression())
    # make param grid
    param_grid = {'logisticregression__C': [0.01, 0.1, 1, 10, 100]}

    # create and fit the model
    model = GridSearchCV(pipe, param_grid, cv=5)
    model.fit(X_train,Y_train)

    # make prediction and print accuracy
    prediction = model.predict(X_test)
    print(f"Accuracy score is {accuracy_score(Y_test, prediction):.2f}")
    print(f"Confusion_matrix is {confusion_matrix(Y_test, prediction)}")
    print(classification_report(Y_test, prediction))
    pickle.dump(model, open('model.pkl', 'wb'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description= "Input your desired data to be passed")
    parser.add_argument('--DataPath', type = str,
    help = 'Enter the data you want to upload here')
    args = parser.parse_args()
    training(args.DataPath)