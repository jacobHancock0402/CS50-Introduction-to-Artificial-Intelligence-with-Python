import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)
    # Bug here when getting corrects and incorrects
    # Maybe because i'm loading labels into lists instead of loading it all in one list
    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    counter = 0
    labels = list()
    temp = list()
    tempo = list()
    evidence = list()
    # Dictionary that maps a value the abbreviation of a month
    months = {
        "Jan" : 0,
        "Feb" : 1,
        "Mar" : 2,
        "Apr" : 3,
        "May" : 4,
        "June" : 5,
        "Jul" : 6,
        "Aug" : 7,
        "Sep" : 8,
        "Oct" : 9,
        "Nov" : 10,
        "Dec" : 11,
    }
    # Open's csv
    with open("shopping.csv") as csv_file:
        reader = csv.reader(csv_file)
        dude = next(reader)
        # Loops through each row
        for row in reader:
            # Loops through each element in the row
            for x in range(len(row)):
                # If x is at one of the index's, the value must be converted to float
                if x == 1 or x == 3 or (x >= 5 and x <= 9):
                    temp.insert(x,float(row[x]))
                # Dictionary is called to get a value for the month in x's position
                elif x == 10:
                    temp.insert(x,months[row[x]])
                # Insert 1 if person is a return visistor, else 0 if they are new
                elif x == 15:
                    if row[x] == "Returning_Visitor":
                        temp.insert(x,1)
                    else:
                        temp.insert(x,0)
                # Insert 0 is person shopped on weekend, or 1 if they didn't
                elif x == 16:
                    if row[x] == "FALSE":
                        temp.insert(x,0)
                    else:
                        temp.insert(x,1)
                # Checks final column to see if they made a purchase. If they did, 1 is added to the label list
                elif x == 17:
                    if row[x] == "FALSE":
                        tempo.insert(x,0)
                    else:
                        tempo.insert(x,1)
                else:
                    temp.insert(x,row[x])
            # After every row, a new list is added to the evidence and labels lists
            evidence.insert(counter,temp)
            labels.insert(counter,tempo)
            temp = list()
            tempo = list()
            counter += 1
    # Evidence and labels lists are paired in a tuple and then returned
    load = (evidence,labels)
    return load





def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Nearest neighbor model is created
    model = KNeighborsClassifier(n_neighbors=1)
    # Model is fit to the data and returned
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    spec = 0
    sens = 0
    counter = 0
    actualSp = 0
    actualSe = 0
    # Loops through every list in labels
    for x in range(len(labels)):
        # If label is 1, positive count is increased by 1
        if labels[x][0] == 1:
            actualSe += 1
            # If prediction is correct, count of positive correct is increased by 1
            if labels[x][0] == predictions[x]:
                sens += 1
        # Same as above but for negative count
        if labels[x][0] == 0:
            actualSp += 1
            if labels[x][0] == predictions[x]:
                spec += 1
        counter += 1
    # Finds proportion of predictions for positive and negative labels that were correct
    trueSens = sens / actualSe
    trueSpec = spec / actualSp
    values = {trueSens, trueSpec}
    return values


if __name__ == "__main__":
    main()
