import json
import numpy as np


if __name__ == "__main__":
    file = open("Statistic_Parameter.json", "r", encoding = "utf-8")
    file_out = open("dataset.csv", "w", encoding="utf-8")
    result = json.load(file)
    for i in range(len(result['class'])):
        if result['class'][i] == "cold-flu":
            result['class'][i] = 0
        else:
            result['class'][i] = 1
    list = []
    for i in range(len(result['class'])):
        temp = 1
        if result['answer_number'][i] > 0:
            temp = 1
        else:
            temp = 0
        list.append(temp)

    result['answer_or_not'] = list
    for i in range(len(result['class'])):
        for key in result.keys():
            file_out.write("%d,"%result[key][i])
        file_out.write("\n")
    file_out.close()
    print(result.keys())
    print(len(result.keys()))
    print(len(result['class']))


