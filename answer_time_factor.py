import json


if __name__ == "__main__":
    file = open("General Health/General -Health-Question.txt", "r")
    answer_times = {}
    j = 0

    while True:
        print(j)
        line = file.readline()
        if not line:
            break
        j += 1
        line = line.strip()
        question = json.loads(line)
        if "answers" not in question.keys():
            print(question)
            continue

        for i in range(len(question["answers"])):
            try:
                answer = question["answers"][i]
                if answer not in answer_times.keys():
                    answer_times[answer] = []
                answer_times[answer].append(int(question["answer_time"][i]))
            except:
                print("no good")

    output = open("answer_time.json", "w")
    json.dump(answer_times, output)
    output.close()