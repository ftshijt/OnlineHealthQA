import re
import requests
import traceback
import json

head = {    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cookie': 'guid=97b6b81de4b87637e6c1654ea99940dfa3693f17; __gads=ID=03d44f7efa080256:T=1507815730:S=ALNI_MaZ7t-7tcT_kM7h8S7UcOFkQ6s7sA; _igg=pW13We3a8ZDcGuLniRk1; sort_by=first_post; _medhelp_session=228981afa02e4c70d02c7a6541203ab3; _ga=GA1.2.1823142418.1507815730; _gid=GA1.2.1872544567.1508510082; s_cc=true; s_sq=%5B%5BB%5D%5D; _gat=1; __ybotb=c4f0; __ybotu=j8oijzc3fly5zxkfvw; __ybotv=1508512486318; __ybots=j901dvvzme78xcnqu9.0.j901dvvywyppxbbavq.1; _igt=2c05c41f-e297-4031-9a46-af5c21ea6c9f; _ig=616321d2-b717-4313-a9de-4ee85ee3e3e5; __ybotc=http%3A//ads-adseast-vpc.yldbt.com/m/; __ybotn=1',
            'Host': 'www.medhelp.org'
            }

def get_communities(list):
    content = []
    if list is []:
        return []
    for l in list:
        temp = re.search(">(.*?)</a>", l, re.S).group(1)
        content.append(temp)
    return content

def get_friends(id, friend_number):
    url = "http://www.medhelp.org/friendships/list/" + id + "?page="
    friend_page = int(int(friend_number) / 24) + 1
    result = []
    try:
        for i in range(1, friend_page + 1):
            url_in = url + "%d"%i
            print("friend")
            html = requests.get(url=url_in, headers=head).text
            friends = re.findall("<div class='login'>(.*?)</div>", html, re.S)
            for friend in friends:
                result.append(re.search('<a href="/personal_pages/user/(.*?)"', friend, re.S).group(1))
    except:
        traceback.print_exc()

    return result

def get_notes(id, notes_number):
    url = "http://www.medhelp.org/notes/list/" + id + "?page="
    note_page = int(int(notes_number) / 32) + 1
    result_notes = []
    result_leavers = []
    result_types = []
    try:
        for i in range(1, note_page + 1):
            url_in = url + "%d"%i
            html = requests.get(url = url_in, headers = head).text
            print("notes")
            notes = re.findall("<div class='note_msg'>(.*?)</div>", html, re.S)
            result_notes.extend(notes)
            note_leavers = re.findall('<div><a href="/personal_pages/user/(.*?)"', html, re.S)
            result_leavers.extend(note_leavers)
            note_types = re.findall('<div title="(.*?)"', html, re.S)
            result_types.extend(note_types)
    except:
        traceback.print_exc()

    return result_notes, result_leavers, result_types

def get_commenters(id, another_id, statues):
    statues_page = int(int(statues) / 10) + 1
    url = "http://www.medhelp.org/personal_pages/" + another_id + "/user_statuses?page="
    result = []
    try:
        for i in range(1, statues_page + 1):
            url_in = url + "%d" % i
            html = requests.get(url=url_in, headers=head).text
            print("commenter")
            comments = re.findall('<a href="/personal_pages/user/(.*?)"', html, re.S)
            for comment in comments:
                if comment == id:
                    continue
                else:
                    result.append(comment)

    except:
        traceback.print_exc()

    return result

def get_person_detail(people_id):
    html = "http://www.medhelp.org/personal_pages/user/" + people_id
    dict = {}
    try:
        text = requests.get(url = html, headers = head).text

        temp = re.search("<span class='title'>About Me:(.*?)/div>", text, re.S).group(1)
        sex_age = re.search("<span>(.*?)/span>", temp, re.S)
        if not sex_age:
            dict['sex'] = ""
            dict['age'] = ""
        else:
            sex_age = sex_age.group(1)
            if sex_age.find("Male") != -1:
                dict['sex'] = 'M'
            elif sex_age.find("Female") != -1:
                dict['age'] = 'F'
            age = re.search('([0-9]+)<', sex_age)
            if not age:
                dict['age'] = ""
            else:
                age = age.group(1)
                dict['age'] = age

        dict['membership'] = re.search("member since (.*?)<", temp, re.S).group(1)
        temp = re.findall("<div><img class='c_disc_icon_xs icon_img_ww' src='/RoR/images/blank.png'>(.*?)</div>", text, re.S)

        dict['communities'] = get_communities(temp)

        dict['notes_number'] = re.search("\$mwidgetHelper.setTitle\('Notes \((.*?)\)", text, re.S)
        if dict['notes_number']:
            dict['notes'], dict['note_leavers'], dict['note_types'] = get_notes(people_id,
                                                                                dict['notes_number'].group(1))
            dict['notes_number'] = int(dict['notes_number'].group(1))
        else:
            dict['notes'] = []
            dict['note_leavers'] = []
            dict['note_types'] = []
            dict['notes_number'] = 0

        dict['posts_number'] = re.search("\$mwidgetHelper.setTitle\('Posts \((.*?)\)", text, re.S)
        if dict['posts_number']:
            dict['posts_number'] = int(dict['posts_number'].group(1))
        else:
            dict['posts_number'] = 0

        dict['friends_number'] = re.search("\$mwidgetHelper.setTitle\('Friends \((.*?)\)", text, re.S)
        if dict['friends_number']:
            dict['friends'] = get_friends(people_id, dict['friends_number'].group(1))
            dict['friends_number'] = int(dict['friends_number'].group(1))
        else:
            dict['friends'] = []
            dict['friends_number'] = 0

        dict['status_number'] = re.search("\$mwidgetHelper.setTitle\('Status \((.*?)\)", text, re.S)
        another_id = re.search("<a href=\"/personal_pages/(.*?)/user_statuses", text, re.S)
        if dict['status_number'] and another_id:
            dict['commenters'] = get_commenters(id, another_id.group(1), dict['status_number'].group(1))
            dict['status_number'] = int(dict['status_number'].group(1))
        else:
            dict['commenters'] = []
            dict['status_number'] = 0
    except:
        traceback.print_exc()

    return dict

def main():
    file = open("breast cancer-detail2.txt", "r", encoding = "utf-8")
    index = {}
    j = 0
    while 1:
        j = j + 1
        print("okok%d"%j)
        line = file.readline()
        #if j <=401:
        #    continue
        if not line:
            break
        try:
            line.strip('\n')
            result = json.loads(line)
            dict = get_person_detail(result['asker'])
            if result['asker'] not in index.keys():
                file_out = open(result['asker'] + ".txt", "w")
                json_dict = json.dumps(dict)
                file_out.write(json_dict)
                print(dict)
                file_out.write('\n')
                file_out.close()
            index[result['asker']] = 0
        except:
            traceback.print_exc()
        if result['answers'] == []:
            continue

        for answer in result['answers']:
            try:
                print(answer)
                if answer not in index.keys():
                    dict = get_person_detail(answer)
                    file_out = open(answer + ".txt", "w")
                    json_dict = json.dumps(dict)
                    file_out.write(json_dict)
                    print(dict)
                    file_out.write('\n')
                    file_out.close()
                index[answer] = 0
            except:
                traceback.print_exc()


main()