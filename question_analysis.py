import re
import requests
import json
import traceback
import time

class question(object):
    def __init__(self):
        self.title = ""
        self.asker = ""
        self.answer = []
        self.Q = ""
        self.follow = ""


head = {    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cookie': 'guid=97b6b81de4b87637e6c1654ea99940dfa3693f17; __gads=ID=03d44f7efa080256:T=1507815730:S=ALNI_MaZ7t-7tcT_kM7h8S7UcOFkQ6s7sA; _igg=pW13We3a8ZDcGuLniRk1; sort_by=first_post; _medhelp_session=228981afa02e4c70d02c7a6541203ab3; _ga=GA1.2.1823142418.1507815730; _gid=GA1.2.1872544567.1508510082; s_cc=true; s_sq=%5B%5BB%5D%5D; _gat=1; __ybotb=c4f0; __ybotu=j8oijzc3fly5zxkfvw; __ybotv=1508512486318; __ybots=j901dvvzme78xcnqu9.0.j901dvvywyppxbbavq.1; _igt=2c05c41f-e297-4031-9a46-af5c21ea6c9f; _ig=616321d2-b717-4313-a9de-4ee85ee3e3e5; __ybotc=http%3A//ads-adseast-vpc.yldbt.com/m/; __ybotn=1',
            'host': 'www.medhelp.org'
            }

def get_a_content(list):
    content = []
    for l in list:
        temp = re.search("style='text-decoration:none'>(.*?)</div>", l, re.S).group(1)
        content.append(temp)
    return content

def get_answer(list):
    content = []
    for l in list:
        temp = re.search('<a href="/personal_pages/user/(.*?)"', l, re.S).group(1)
        content.append(temp)
    return content

def get_a_upvote(list):
    content = []
    for l in list:
        temp = re.search("<span id=user_rating_count_Post_(.*?)/span>", l, re.S).group(1)
        temp2 = re.search(">(.*?)<", temp, re.S).group(1)
        content.append(temp2)
    return content

def get_a_time(list):
    content = []
    for l in list:
        temp = re.search("<span class='mh_timestamp' data-timestamp='(.*?)'", l, re.S).group(1)
        content.append(temp)
    return content


def get_detail(url):
    dict = {}
    html = requests.get(url=url, headers=head).text
    #print(html)
    try:

        dict['title'] = re.search("<title>(.*?)</title>", html, re.S).group(1)
        temp = re.search('<div id="posts_wrapper">(.*?)<div class="subj_info os_14 ">', html, re.S).group(1)
        dict['question'] =re.search("style='text-decoration:none'>(.*?)</div>", temp, re.S).group(1)
        dict['answer_number'] = re.search('<a href="#post_answer_header" id="answer_scroll">(.*?) Answer', html, re.S).group(1)
        temp = re.search('div class="tertiary_btn_ctn flex "(.*?)div class="mh_tertiary_btn"', html, re.S).group(1)
        temp2 = re.search('<span id=user_rating_count_Post(.*?)/span>', temp, re.S).group(1)
        dict['upvotes'] = re.search('>(.*?)<', temp2, re.S).group(1)
        temp = re.search('<div id="posts_wrapper">(.*?)<img alt="', html, re.S).group(1)
        dict['asker'] = re.search('<a href="/personal_pages/user/(.*?)">', temp, re.S).group(1)
        temp = re.findall("<span class='mh_timestamp' data-timestamp='(.*?)'", html, re.S)
        dict['time'] = temp[0]
        temp = re.findall('<div class="post_entry_wrapper">(.*?)<div class="comments empty">', html, re.S)
        tempx = re.findall('<div class="post_entry_wrapper">(.*?)<div class="comments ">', html, re.S)
        #print(tempx)
        if tempx != []:
            print("here")
            temp.extend(tempx)
        #print(temp)
        if temp is None:
            dict['answer_time'] = []
            dict['answers'] = []
            dict['answers_conent'] = []
            dict['answer_upvote'] = []
            return dict
        dict['answers'] = get_answer(temp)
        dict['answers_conent'] = get_a_content(temp)
        dict['answer_upvote'] = get_a_upvote(temp)
        dict['answer_time'] = get_a_time(temp)
        print("ok")
    except:
        traceback.print_exc()
        print(url)
    return dict


def main():
    file = open("depression.txt", "r")
    filex = open("temp.txt", "w+")
    i = 0
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            print(line)
            print(i)

            try: #1349
                if i > 1349:
                    i = i + 1
                    continue
                dict = get_detail("http://" + line.strip('\n'))
                json_temp = json.dumps(dict)
                filex.write(json_temp)
                filex.write("\n")
                i = i + 1
            except:
                traceback.print_exc()
                continue



main()