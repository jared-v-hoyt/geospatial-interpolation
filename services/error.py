import csv
import math


def calculate_error(file_path):
    observed, predicted = [], []

    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            observed.append(float(row[2])) 
            predicted.append(float(row[3]))

    n = len(observed)
    mae = sum(abs(obs - pred) for obs, pred in zip(observed, predicted)) / n
    rmse = math.sqrt(sum((obs - pred) ** 2 for obs, pred in zip(observed, predicted)) / n)
    mse = sum((obs - pred) ** 2 for obs, pred in zip(observed, predicted)) / n

    return mae, rmse, mse