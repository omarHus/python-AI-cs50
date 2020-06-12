import csv
import sys
import pandas as pd
from enum import Enum

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# Enum for Month
class Month(Enum):
    Jan  = 0
    Feb  = 1
    Mar  = 2
    Apr  = 3
    May  = 4
    June = 5
    Jul  = 6
    Aug  = 7
    Sep  = 8
    Oct  = 9
    Nov  = 10
    Dec  = 11

def VisitorType(visitor):
    if visitor == "Returning_Visitor":
        return 1
    else:
        return 0


def bool_to_int(boolean):
    if boolean == "TRUE":
        return 1
    else:
        return 0



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

    # Read csv file
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        evidence = []
        labels   = []

        # Parse data by rows
        for row in csv_reader:
            e = []

            # separate data into evidence and labels
            e.append(int(row["Administrative"]))
            e.append(float(row["Administrative_Duration"]))
            e.append(int(row["Informational"]))
            e.append(float(row["Informational_Duration"]))
            e.append(int(row["ProductRelated"]))
            e.append(float(row["ProductRelated_Duration"]))
            e.append(float(row["BounceRates"]))
            e.append(float(row["ExitRates"]))
            e.append(float(row["PageValues"]))
            e.append(float(row["SpecialDay"]))
            e.append(Month[row["Month"]].value)
            e.append(int(row["OperatingSystems"]))
            e.append(int(row["Browser"]))
            e.append(int(row["Region"]))
            e.append(int(row["TrafficType"]))
            e.append(VisitorType(row["VisitorType"]))
            e.append(bool_to_int(row["Weekend"]))
            evidence.append(e)

            labels.append(bool_to_int(row["Revenue"]))
        
    return ((evidence, labels))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create model
    model = KNeighborsClassifier(n_neighbors=1)

    # train model
    model.fit(evidence, labels)

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

    num_of_pred_pos = 0
    num_of_pred_neg = 0

    for label, prediction in zip(labels, predictions):
        if label == prediction:
            if label == 1:
                num_of_pred_pos += 1
            else:
                num_of_pred_neg += 1
    
    sensitivity = num_of_pred_pos/labels.count(1)
    specificity = num_of_pred_neg/list(predictions).count(0)

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
