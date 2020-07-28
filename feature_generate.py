import json
import traceback
import re
from textblob import *
import csv
import requests

check_class = [" Adults with Special Needs ", " Chronic Fatigue Syndrome ", " Cold &amp; Flu ", " Disaster Preparedness ",
               " Emphysema ", " Eye Care ", " General Health ", " General Surgery ", " Hemorrhoids ",
               " Occupational Health &amp; Safety ", " Radiology  ", " Stress ", " Swine Flu ", " Undiagnosed Symptoms ",
               " Vitamin D ", " Vitamins &amp; Supplements "]
feature_list = ["CWC", "CS", "AP", "AS", "VP", "VS", "TWC", "TCS",
                "TAP", "TAS", "TVP", "TVS", "C1", "C2", "C3", "C4",
                "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
                "C13", "C14", "C15", "C16", "A", "MEM", "NN", "FN",
                "PN", "SN", "FNDC", "FNBC", "FNEC", "FNCC", "FNLC", "FNP",
                "CNDC", "CNBC", "CNEC", "CNCC", "CNLC", "CNP", "NNDC", "NNBC",
                "NNEC", "NNCC", "NNLC", "NNP", "AB", "GFIC", "AN"]
def content_cleaning(content):
    content = content.replace("&#39;", "'")
    content = content.replace("&nbsp;", " ")
    content = content.replace("<br/>", " ")
    content = content.replace("\n", " ")
    content = content.replace("\r", " ")
    content = content.replace("&amp;", "&")
    temp = content.replace("  ", " ")
    while content != temp:
        content = content.replace("  ", " ")
        temp = content.replace("  ", " ")
    content = content.strip(" ")
    return content

def get_class(feature, check):
    list = [0] * len(check)
    i = 0
    print(feature)
    for c in check:
        if c == feature:
            list[i] = 1
            break
        i+=1
    return list

def check_category(category):
    for c in category:
        if c == 1:
            return True
    return False

def get_content_feature(content):
    result = []
    blob = TextBlob(content)
    sentences = len(blob.sentences)
    word_count = len(re.findall(" ", content, re.S)) + 1
    result.append(word_count)
    result.append(sentences)
    sum1 = 0
    sum2 = 0
    for sentence in blob.sentences:
        polarity = sentence.sentiment.polarity
        subjectivity = sentence.sentiment.subjectivity
        if polarity == 0 and subjectivity == 0:
            continue
        sum1 += polarity
        sum2 += subjectivity

    avg_polarity = sum1 / sentences
    avg_subjectivity = sum2 / sentences
    result.append(avg_polarity)
    result.append(avg_subjectivity)

    sumx = 0
    sumy = 0
    if sentences > 1:
        for sentence in blob.sentences:
            polarity = sentence.sentiment.polarity
            subjectivity = sentence.sentiment.subjectivity
            if polarity == 0 and subjectivity == 0:
                continue
            sumx += polarity - avg_polarity
            sumy = subjectivity - avg_subjectivity

        var_polarity = sumx * sumx / (sentences - 1)
        var_subjectivity = sumy * sumy / (sentences - 1)
    else:
        var_polarity = 0
        var_subjectivity = 0
    result.append(var_polarity)
    result.append(var_subjectivity)

    content = re.sub("[^ a-zA-Z]", "", content, flags=re.S)
    words = content.split(" ")
    complex_word = 0
    for word in words:
        if word.upper() not in cmu_dict.keys():
            continue
        if cmu_dict[word.upper()] >= 3:
            complex_word += 1
    fog = 0.4 * (word_count / sentences + 100 * complex_word / word_count)
    return result, fog


def cmu_dict_load():
    vowels_text = open("vowels.txt", "r", encoding="utf-8")
    line = vowels_text.readline()
    vowels_text.close()
    line = line.strip()
    vowels = line.split(" ")
    cmu_dict = {}
    cmu_dict_text = open("cmd_dict.txt", "r", encoding="utf=8")
    while True:
        line = cmu_dict_text.readline()
        if not line:
            break
        line = line.strip()
        line = line.split("  ")
        phones = line[1].split(" ")
        syllables = 0
        for phone in phones:
            if phone in vowels:
                syllables += 1
        cmu_dict[line[0]] = syllables
    return cmu_dict



if __name__ == "__main__":
    file = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\General -Health-Question.txt", "r")
    error_log = open("error.log", "w")
    out_csv = csv.writer(open("feature_csv_20190108.csv", "w", newline=""))
    out_csv.writerow(feature_list)
    j = 0
    Feature = {}
    cmu_dict = cmu_dict_load()
    for f in feature_list:
        Feature[f] = []
    friend = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\Friend_Parameter.json", "r")
    friend = json.load(friend)
    comment = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\Commenter_Parameter.json", "r")
    comment = json.load(comment)
    note = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\Notes_Parameter.json", "r")
    note = json.load(note)
    answer_times = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\answer_time.json", "r")
    answer_times = json.load(answer_times)
    last_category = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while True:
        print(j)
        line = file.readline()
        if not line:
            break
        try:
            question = json.loads(line)

        except:
            traceback.print_exc()
            break
        try:
            single_feature = []
            question_content = content_cleaning(question["question"])
            content_feature, fog = get_content_feature(question_content)
            # (6) --- word_count, sentences, avg_p, avg_s, var_p, var_s
            title = re.search("(.*?)-", question["title"], re.S).group(1)
            title_feature, dummy_fog = get_content_feature(title)
            # (6) --- word_count, sentences, avg_p, avg_s, var_p, var_s
            cate = re.findall("-(.*?)-", question["title"], re.S)[-1]
            category = get_class(cate, check_class)
            if check_category(category):
                last_category = category
            else:
                category = last_category
            # (16) --- one-hot encoding category
            single_feature.extend(content_feature)
            single_feature.extend(title_feature)
            single_feature.extend(category)
            asker = question['asker']
            with open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\PEOPLE\\"
                      + asker + ".txt", "r") as ask:
                user = json.load(ask)
                age = user["age"]
                if age == "":
                    age = -1
                else:
                    age = int(age)
                membership = int(content_cleaning(user["membership"])[4:])
                notes_number = int(user['notes_number'])
                communities = len(user['communities'])
                friends_number = int(user['friends_number'])
                posts_number = int(user['posts_number'])
                status_number = int(user['status_number'])
                single_feature.append(age)
                single_feature.append(membership)
                single_feature.append(notes_number)
                single_feature.append(friends_number)
                single_feature.append(posts_number)
                single_feature.append(status_number)

            single_feature.append(friend[asker]["degree_centrality"])
            single_feature.append(friend[asker]["betweenness_centrality"])
            single_feature.append(friend[asker]["eigenvector_centrality"])
            single_feature.append(friend[asker]["closeness_centrality"])
            single_feature.append(friend[asker]["load_centrality"])
            single_feature.append(friend[asker]["pagerank"])

            single_feature.append(comment[asker]["degree_centrality"])
            single_feature.append(comment[asker]["betweenness_centrality"])
            single_feature.append(comment[asker]["eigenvector_centrality"])
            single_feature.append(comment[asker]["closeness_centrality"])
            single_feature.append(comment[asker]["load_centrality"])
            single_feature.append(comment[asker]["pagerank"])

            single_feature.append(note[asker]["degree_centrality"])
            single_feature.append(note[asker]["betweenness_centrality"])
            single_feature.append(note[asker]["eigenvector_centrality"])
            single_feature.append(note[asker]["closeness_centrality"])
            single_feature.append(note[asker]["load_centrality"])
            single_feature.append(note[asker]["pagerank"])

            time = int(question["time"])
            pre_answer = 0
            if asker in answer_times.keys():
                for t in answer_times[asker]:
                    if t < time:
                        pre_answer += 1
            single_feature.append(pre_answer)

            # try:
            #     data = {'text': question_content}
            #     rfog = requests.post("http://www.gunning-fog-index.com/fog.cgi", data=data)
            #     fogs = re.findall('Gunning Fog index is <FONT COLOR="red">(.*?) </FONT>', rfog.text, re.S)
            #     fog = float(fogs[0])
            # except:
            #     fog = 0
            print("fog:" + str(fog))
            single_feature.append(fog)
            try:
                single_feature.append(int(question["answer_number"]))
            except:
                number = re.findall(">(.*?)<", question["answer_number"], re.S)
                number = int(number[0])
                single_feature.append(number)
            out_csv.writerow(single_feature)
            index = 0
            # print(single_feature)
            for f in feature_list:
                Feature[f].append(single_feature[index])
                index += 1
        except:
            traceback.print_exc()
            error_log.write("%d\n"%j)
            error_log.flush()
        j = j + 1
    output = open("Feature_20190108.json", "w")
    json.dump(Feature, output)
    output.close()