import json
import traceback
import re
from textblob import *
import csv

def extractor(file):
    csv_reader = csv.reader(file)
    flag = 0
    person = {}
    for row in csv_reader:
        if flag == 0:
            flag = 1
            continue
        person[row[1]] = row
    return person

if __name__ =="__main__":
    #nltk.download('punkt')
    file = open("cold-flu\\cold-flu-detail.txt", "r", encoding="utf-8")
    graph_para = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\cold-flu\\cold-flu.csv", "r", encoding="utf-8")
    file_out = open("Statistic_New_Parameter.json", "w", encoding="utf-8")
    j = 0

    final_answer_number = []
    final_word_count = []
    final_word_count_title = []
    final_notes_number = []
    final_friends_number = []
    final_posts_number = []
    final_status_number = []
    final_avg_polarity = []
    final_avg_subjectivity = []
    final_var_polarity = []
    final_var_subjectivity = []
    final_sentences = []
    final_class = []
    final_communities = []
    final_degree = []
    final_authority = []
    final_eccentricity = []
    final_closnesscentrality = []
    final_pageranks = []
    final_eigencentrality = []
    graph_extract = extractor(graph_para)
    print(graph_extract)
    while True:
        try:
            j = j + 1
            print("okok%d" % j)
            line = file.readline()
            if not line:
                break
            result = json.loads(line)

            answer_number = int(result['answer_number'])
            answer_name = result['answers']
            question = result['question']
            word_count = len(re.findall(" ", question, re.S)) + 1

            title = result['title']
            word_count_title = len(re.findall(" ", title, re.S)) + 1
            asker = result['asker']
            print(asker)
            file_asker = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\cold-flu\\" + asker + ".txt",
                              "r", encoding="utf-8")
            asker_detail = json.load(file_asker)
            file_asker.close()
            notes_number = int(asker_detail['notes_number'])
            communities = len(asker_detail['communities'])
            friends_number = int(asker_detail['friends_number'])
            posts_number = int(asker_detail['posts_number'])
            status_number = int(asker_detail['status_number'])
            friends = asker_detail['friends']
            blob = TextBlob(question)
            sentences = len(blob.sentences)
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
            try:
                final_authority.append(float(graph_extract[asker][14]))
                final_eccentricity.append(float(graph_extract[asker][9]))
                final_closnesscentrality.append(float(graph_extract[asker][10]))
                final_pageranks.append(float(graph_extract[asker][16]))
                final_eigencentrality.append(float(graph_extract[asker][20]))
            except:
                final_authority.append(0)
                final_eccentricity.append(0)
                final_closnesscentrality.append(0)
                final_pageranks.append(0)
                final_eigencentrality.append(0)
            final_answer_number.append(answer_number)
            final_word_count.append(word_count)
            final_word_count_title.append(word_count_title)
            final_posts_number.append(posts_number)
            final_status_number.append(status_number)
            final_notes_number.append(notes_number)
            final_friends_number.append(friends_number)
            final_avg_polarity.append(avg_polarity)
            final_avg_subjectivity.append(avg_subjectivity)
            final_var_polarity.append(var_polarity)
            final_var_subjectivity.append(var_subjectivity)
            final_sentences.append(sentences)
            final_class.append("cold-flu")
            final_communities.append(communities)
        except:
            traceback.print_exc()


    file.close()
    file = open("stress\\stress_detail.txt", "r", encoding="utf-8")
    graph_para = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\stress\\stress.csv", "r", encoding="utf-8")
    graph_extract = extractor(graph_para)
    while True:
        try:
            j = j + 1
            print("okok%d" % j)
            line = file.readline()
            if not line:
                break
            result = json.loads(line)

            answer_number = int(result['answer_number'])
            answer_name = result['answers']
            question = result['question']

            word_count = len(re.findall(" ", question, re.S)) + 1
            title = result['title']
            word_count_title = len(re.findall(" ", title, re.S)) + 1
            asker = result['asker']
            print(asker)
            file_asker = open("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\stress\\" + asker + ".txt",
                              "r", encoding="utf-8")
            asker_detail = json.load(file_asker)
            file_asker.close()
            notes_number = int(asker_detail['notes_number'])
            friends_number = int(asker_detail['friends_number'])
            posts_number = int(asker_detail['posts_number'])
            communities = len(asker_detail['communities'])
            status_number = int(asker_detail['status_number'])
            friends = asker_detail['friends']
            blob = TextBlob(question)
            sentences = len(blob.sentences)
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

            try:
                final_authority.append(float(graph_extract[asker][14]))
                final_eccentricity.append(float(graph_extract[asker][9]))
                final_closnesscentrality.append(float(graph_extract[asker][10]))
                final_pageranks.append(float(graph_extract[asker][16]))
                final_eigencentrality.append(float(graph_extract[asker][20]))
            except:
                final_authority.append(0)
                final_eccentricity.append(0)
                final_closnesscentrality.append(0)
                final_pageranks.append(0)
                final_eigencentrality.append(0)
            final_answer_number.append(answer_number)
            final_word_count.append(word_count)
            final_word_count_title.append(word_count_title)
            final_posts_number.append(posts_number)
            final_status_number.append(status_number)
            final_notes_number.append(notes_number)
            final_friends_number.append(friends_number)
            final_avg_polarity.append(avg_polarity)
            final_avg_subjectivity.append(avg_subjectivity)
            final_var_polarity.append(var_polarity)
            final_var_subjectivity.append(var_subjectivity)
            final_sentences.append(sentences)
            final_class.append("stress")
            final_communities.append(communities)
        except:
            traceback.print_exc()

    dict = {
        'answer_number': final_answer_number,
        'word_count': final_word_count,
        'word_count_title': final_word_count_title,
        'posts_number': final_posts_number,
        'status_number': final_status_number,
        'notes_number': final_notes_number,
        'friend_number': final_friends_number,
        'avg_p': final_avg_polarity,
        'avg_s': final_avg_subjectivity,
        'var_p': final_var_polarity,
        'var_s': final_var_subjectivity,
        'sentences': final_sentences,
        'class': final_class,
        'communities':final_communities,
        'authority':final_authority,
        'eccentricity':final_eccentricity,
        'closnesscentrality':final_closnesscentrality,
        'page_rank':final_pageranks,
        'eigencentrality':final_eigencentrality,
    }
    json_dict = json.dumps(dict)
    file_out.write(json_dict)
    file_out.close()
    file.close()




